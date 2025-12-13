use pyo3::prelude::*;
use pyo3::exceptions;
use pyo3::types::PyList;

use ark_bls12_381::{Fq, G1Affine};
use ark_serialize::{CanonicalSerialize, CanonicalDeserialize};
use ark_relations::r1cs::ConstraintMatrices;
use ark_ff::{Zero, One, PrimeField, UniformRand};
use ark_crypto_primitives::sponge::{CryptographicSponge, FieldBasedCryptographicSponge};
use rand_core::OsRng;

use crate::arithmetization::Arithmetization;
use crate::r1cs::R1CS;
use crate::create_generators;

fn pyany_to_fq(obj: &pyo3::PyAny) -> PyResult<Fq> {
    use ark_ff::BigInteger384;
    use pyo3::{exceptions, PyErr};
    use pyo3::types::PyBytes;    

    if let Ok(b) = obj.downcast::<PyBytes>() {
        let slice = b.as_bytes();

        if slice.len() > 48 {
            return Err(PyErr::new::<exceptions::PyValueError, _>(
                "field element bytes too large",
            ));
        }

        let mut padded = [0u8; 48];
        padded[48 - slice.len()..].copy_from_slice(slice);

        let mut rdr = &padded[..];
        let bi = BigInteger384::deserialize_compressed_unchecked(&mut rdr)
            .map_err(|_| PyErr::new::<exceptions::PyValueError, _>("invalid bigint"))?;

        let fq = Fq::from_bigint(bi)
            .ok_or_else(|| PyErr::new::<exceptions::PyValueError, _>("invalid Fq element"))?;

        return Ok(fq);
    }

    if let Ok(i) = obj.extract::<u128>() {
        return Ok(Fq::from(i));
    }

    if let Ok(s) = obj.extract::<String>() {
        let s_trim = s.trim();

        if s_trim.starts_with("0x") {
            let hex = &s_trim[2..];
            let bytes = hex::decode(hex)
                .map_err(|_| PyErr::new::<exceptions::PyValueError, _>("bad hex"))?;
            let pyb = PyBytes::new(obj.py(), &bytes);
            return pyany_to_fq(pyb);
        }

        if let Ok(v) = s_trim.parse::<u128>() {
            return Ok(Fq::from(v));
        }

        return Err(PyErr::new::<exceptions::PyValueError, _>("bad field string"));
    }

    Err(PyErr::new::<exceptions::PyTypeError, _>(
        "field element must be bytes/int/string",
    ))
}

fn py_tuple_to_pair(elem: &pyo3::PyAny) -> PyResult<(Fq, usize)> {
    let seq = elem.extract::<(pyo3::PyObject, pyo3::PyObject)>()?;
    Python::with_gil(|py| {
        let a = seq.0.as_ref(py);
        let b = seq.1.as_ref(py);
        let fq = pyany_to_fq(a)?;
        let idx = b.extract::<usize>().map_err(|e| PyErr::new::<exceptions::PyTypeError, _>(format!("invalid index: {}", e)))?;
        Ok((fq, idx))
    })
}

fn py_matrix_to_sparse(_py: Python, obj: &PyAny) -> PyResult<Vec<Vec<(Fq, usize)>>> {
    let rows: &PyList = obj.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("Expected a list of rows"))?;
    let mut out = Vec::with_capacity(rows.len());
    for row in rows.iter() {
        let row_list: &PyList = row.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("Expected row to be a list"))?;
        let mut rvec = Vec::with_capacity(row_list.len());
        for entry in row_list.iter() {
            let pair = py_tuple_to_pair(entry)?;
            rvec.push(pair);
        }
        out.push(rvec);
    }
    Ok(out)
}

#[pyfunction]
fn r1cs_from_python(
    py: Python,
    a: &PyAny,
    b: &PyAny,
    c: &PyAny,
    num_instance_vars: usize,
    num_witness_vars: usize,
    instance_vals: Option<&PyAny>,
    witness_vals: Option<&PyAny>,
    z0: Option<&PyAny>,
) -> PyResult<PyObject> {
    let a_s = py_matrix_to_sparse(py, a)?;
    let b_s = py_matrix_to_sparse(py, b)?;
    let c_s = py_matrix_to_sparse(py, c)?;

    let num_constraints = a_s.len();

    let matrices = ConstraintMatrices::<Fq> {
        num_instance_variables: num_instance_vars,
        num_witness_variables: num_witness_vars,
        num_constraints,
        a_num_non_zero: a_s.iter().map(|r| r.len()).sum(),
        b_num_non_zero: b_s.iter().map(|r| r.len()).sum(),
        c_num_non_zero: c_s.iter().map(|r| r.len()).sum(),
        a: a_s,
        b: b_s,
        c: c_s,
    };

    let instance_vec: Vec<Fq> = if let Some(inst_any) = instance_vals {
        let inst_list: &PyList = inst_any.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("instance must be a list"))?;
        inst_list.iter().map(|x| pyany_to_fq(x)).collect::<PyResult<Vec<Fq>>>()?
    } else {
        vec![]
    };
    let witness_vec: Vec<Fq> = if let Some(w_rx) = witness_vals {
        let w_list: &PyList = w_rx.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("witness must be a list"))?;
        w_list.iter().map(|x| pyany_to_fq(x)).collect::<PyResult<Vec<Fq>>>()?
    } else {
        vec![]
    };

    let z0_vec: Vec<Fq> = if let Some(z0_any) = z0 {
        let zlist: &PyList = z0_any.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("z0 must be a list"))?;
        zlist.iter().map(|x| pyany_to_fq(x)).collect::<PyResult<Vec<Fq>>>()?
    } else {
        vec![]
    };

    let r1cs = R1CS {
        shape: matrices,
        param: Fq::zero(),
        comm_witness: G1Affine::rand(&mut OsRng),
        comm_E: G1Affine::rand(&mut OsRng),
        comm_T: G1Affine::rand(&mut OsRng),
        E: vec![Fq::zero(); num_constraints],
        witness: witness_vec,
        instance: instance_vec,
        u: Fq::one(),
        hash: Fq::zero(),
        output: if !z0_vec.is_empty() { z0_vec } else { vec![Fq::zero()] },
    };

    let pyobj = PyR1CS { inner: r1cs }.into_py(py);
    Ok(pyobj)
}

fn fq_to_bytes(f: &Fq) -> Vec<u8> {
    let mut v = vec![];
    f.serialize_compressed(&mut v).ok();
    v
}

fn g1_to_bytes(p: &G1Affine) -> Vec<u8> {
    let mut v = vec![];
    p.serialize_compressed(&mut v).unwrap();
    v
}

#[pyclass]
#[derive(Clone)]
pub struct PyR1CS {
    inner: R1CS,
}

#[pymethods]
impl PyR1CS {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "PyR1CS(constraints={}, instance_len={}, witness_len={})",
            self.inner.shape.num_constraints,
            self.inner.instance.len(),
            self.inner.witness.len(),
        ))
    }
    
    fn is_satisfied(&self) -> PyResult<bool> {
        Ok(self.inner.is_satisfied(&[]))
    }

    #[getter]
    fn num_constraints(&self) -> PyResult<usize> {
        Ok(self.inner.shape.num_constraints)
    }

    fn witness_bytes(&self) -> PyResult<Vec<Vec<u8>>> {
        Ok(self.inner.witness.iter().map(|f| fq_to_bytes(f)).collect())
    }

    fn instance_bytes(&self) -> PyResult<Vec<Vec<u8>>> {
        Ok(self.inner.instance.iter().map(|f| fq_to_bytes(f)).collect())
    }

    fn witness_commitment_bytes(&self) -> PyResult<Vec<u8>> {
        Ok(g1_to_bytes(&self.inner.comm_witness))
    }

    fn comms_bytes(&self) -> PyResult<(Vec<u8>, Vec<u8>)> {
        Ok((g1_to_bytes(&self.inner.comm_E), g1_to_bytes(&self.inner.comm_T)))
    }

    fn output_bytes(&self) -> PyResult<Vec<Vec<u8>>> {
        Ok(self.inner.output.iter().map(|f| fq_to_bytes(f)).collect())
    }

    fn set_instance_and_witness(&mut self, _py: Python, instance_vals: Option<&PyAny>, witness_vals: Option<&PyAny>) -> PyResult<()> {
        if let Some(inst_any) = instance_vals {
            let inst_list: &PyList = inst_any.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("instance must be a list"))?;
            self.inner.instance = inst_list.iter().map(|x| pyany_to_fq(x)).collect::<PyResult<Vec<Fq>>>()?;
        }
        if let Some(w_rx) = witness_vals {
            let w_list: &PyList = w_rx.downcast::<PyList>().map_err(|_| PyErr::new::<exceptions::PyTypeError, _>("witness must be a list"))?;
            self.inner.witness = w_list.iter().map(|x| pyany_to_fq(x)).collect::<PyResult<Vec<Fq>>>()?;
        }
        Ok(())
    }
}

#[pyclass]
pub struct DynProof {
    constants: ark_crypto_primitives::sponge::poseidon::PoseidonConfig<Fq>,
    generators: Vec<G1Affine>,
    folded: Vec<R1CS>,
    latest: R1CS,
    prev_pc: usize,
    pc: usize,
    i: usize,
}

#[pymethods]
impl DynProof {
    fn __repr__(&self) -> PyResult<String> {
        Ok(format!(
            "DynProof(i={}, pc={}, folded_len={}, latest_constraints={})",
            self.i,
            self.pc,
            self.folded.len(),
            self.latest.shape.num_constraints,
        ))
    }
    
    #[new]
    fn new(py_folded: &PyAny, latest: PyR1CS, generators_count: usize) -> PyResult<Self> {
        let folded_py: Vec<PyR1CS> = py_folded.extract()?;
        let folded: Vec<R1CS> = folded_py.into_iter().map(|p| p.inner).collect();
        
        let constants = {
            let (ark, mds) = ark_crypto_primitives::sponge::poseidon::find_poseidon_ark_and_mds(
                Fq::MODULUS.const_num_bits() as u64,
                2, 8, 43, 0,
            );
            ark_crypto_primitives::sponge::poseidon::PoseidonConfig {
                full_rounds: 8,
                partial_rounds: 43,
                alpha: 5,
                ark,
                mds,
                rate: 2,
                capacity: 1,
            }
        };

        let generators = if let Ok(gens) = std::panic::catch_unwind(|| create_generators(generators_count)) {
            gens
        } else {
            (0..generators_count).map(|_| G1Affine::rand(&mut OsRng)).collect::<Vec<G1Affine>>()
        };

        Ok(Self {
            constants,
            generators,
            folded,
            latest: latest.inner,
            prev_pc: 0,
            pc: 0,
            i: 1,
        })
    }

    #[getter]
    fn i(&self) -> usize { self.i }

    #[setter]
    fn set_i(&mut self, v: usize) { self.i = v; }

    #[getter]
    fn latest(&self) -> PyR1CS {
        PyR1CS { inner: self.latest.clone() }
    }
    
    pub fn verify_latest_r1cs(&self) -> PyResult<bool> {
        Ok(self.latest.is_satisfied(&[]))
    }

    pub fn update_with_latest(&mut self, pc: usize, python_new_latest: PyR1CS) -> PyResult<()> {
        if self.folded.is_empty() {
            return Err(PyErr::new::<exceptions::PyValueError, _>("folded set is empty"));
        }

        let folded_idx = self.pc;
        let params = self.params_sum();
        let new_latest = python_new_latest.inner;

        self.folded[folded_idx].fold(&self.latest, &self.constants, &self.generators, params);

        self.latest = new_latest;
        self.prev_pc = self.pc;
        self.pc = pc;
        self.i += 1;
        Ok(())
    }

    pub fn verify(&self) -> PyResult<()> {
        if self.i == 1 {
            if self.folded.iter().any(|pair| pair.has_crossterms()) {
                return Err(PyErr::new::<exceptions::PyRuntimeError, _>("Expected base case: folded pair has crossterms"));
            }
            if self.latest.has_crossterms() {
                return Err(PyErr::new::<exceptions::PyRuntimeError, _>("Expected base case: latest has crossterms"));
            }
            return Ok(());
        }

        let hash = self.hash_public_io();
        if self.latest.hash() != hash {
            return Err(PyErr::new::<exceptions::PyRuntimeError, _>(format!("Hash mismatch: expected {:?}, got {:?}", hash, self.latest.hash())));
        }

        if self.pc >= self.folded.len() {
            return Err(PyErr::new::<exceptions::PyRuntimeError, _>(format!("PC out of range: {} >= {}", self.pc, self.folded.len())));
        }

        if self.latest.has_crossterms() {
            return Err(PyErr::new::<exceptions::PyRuntimeError, _>("Latest has crossterms unexpectedly"));
        }

        if self.folded.iter().any(|pair| !pair.is_satisfied(&self.generators)) {
            return Err(PyErr::new::<exceptions::PyRuntimeError, _>("One of folded instances is unsatisfied"));
        }
        if !self.latest.is_satisfied(&self.generators) {
            return Err(PyErr::new::<exceptions::PyRuntimeError, _>("Latest instance is unsatisfied"));
        }
        Ok(())
    }

    fn latest_hash_bytes(&self) -> PyResult<Vec<u8>> {
        let mut v = vec![];
        self.latest.hash().serialize_compressed(&mut v).map_err(|e| PyErr::new::<exceptions::PyRuntimeError, _>(format!("{:?}", e)))?;
        Ok(v)
    }
}

impl DynProof {
    pub(crate) fn params_sum(&self) -> Fq {
        self.folded
            .iter()
            .map(|p| p.params())
            .fold(Fq::zero(), |acc, x| acc + x)
    }

    pub(crate) fn hash_public_io(&self) -> Fq {
        use ark_crypto_primitives::sponge::poseidon::PoseidonSponge;
        let mut sponge = PoseidonSponge::<Fq>::new(&self.constants);
        sponge.absorb(&vec![self.params_sum()]);
        sponge.absorb(&vec![Fq::from(self.i as u64)]);
        sponge.absorb(&vec![Fq::from(self.pc as u64)]);

        let prev = &self.folded[self.prev_pc];
        for z in prev.z0() { sponge.absorb(&vec![z]); }
        for out in prev.output() { sponge.absorb(&vec![*out]); }

        let wc = prev.witness_commitment();
        sponge.absorb(&vec![wc.x, wc.y, Fq::from(wc.infinity)]);

        for ct in prev.crossterms() { sponge.absorb(&vec![ct]); }
        sponge.absorb(&vec![prev.hash()]);

        sponge.squeeze_native_field_elements(1)[0]
    }
}

#[pyfunction]
fn make_empty_proof(r1cs: PyR1CS, generators_count: usize) -> PyResult<DynProof> {
    let folded = vec![r1cs.inner.clone()];
    let constants = {
        let (ark, mds) = ark_crypto_primitives::sponge::poseidon::find_poseidon_ark_and_mds(
            Fq::MODULUS.const_num_bits() as u64,
            2, 8, 43, 0,
        );
        ark_crypto_primitives::sponge::poseidon::PoseidonConfig {
            full_rounds: 8,
            partial_rounds: 43,
            alpha: 5,
            ark,
            mds,
            rate: 2,
            capacity: 1,
        }
    };

    let generators = create_generators(generators_count);

    Ok(DynProof {
        constants,
        generators,
        folded,
        latest: r1cs.inner.clone(),
        prev_pc: 0,
        pc: 0,
        i: 1,
    })
}

#[pymodule]
fn seminova(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<PyR1CS>()?;
    m.add_class::<DynProof>()?;
    m.add_function(wrap_pyfunction!(r1cs_from_python, m)?)?;
    m.add_function(wrap_pyfunction!(make_empty_proof, m)?)?;
    Ok(())
}
