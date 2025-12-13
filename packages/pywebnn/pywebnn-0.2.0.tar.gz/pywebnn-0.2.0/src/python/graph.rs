//! Compiled computational graph representation
//!
//! PyO3 macros generate unsafe code that triggers unsafe_op_in_unsafe_fn warnings.
//! This is expected behavior from the macro-generated code.
#![allow(unsafe_op_in_unsafe_fn)]

use crate::graph::GraphInfo;
use pyo3::prelude::*;

/// Represents a compiled computational graph
#[pyclass(name = "MLGraph")]
pub struct PyMLGraph {
    pub(crate) graph_info: GraphInfo,
}

#[pymethods]
impl PyMLGraph {
    fn __repr__(&self) -> String {
        format!(
            "MLGraph(operands={}, operations={})",
            self.graph_info.operands.len(),
            self.graph_info.operations.len()
        )
    }

    /// Get the number of operands in the graph
    #[getter]
    fn operand_count(&self) -> usize {
        self.graph_info.operands.len()
    }

    /// Get the number of operations in the graph
    #[getter]
    fn operation_count(&self) -> usize {
        self.graph_info.operations.len()
    }

    /// Get input names
    fn get_input_names(&self) -> Vec<String> {
        self.graph_info
            .operands
            .iter()
            .filter_map(|op| {
                if matches!(op.kind, crate::graph::OperandKind::Input) {
                    op.name.clone()
                } else {
                    None
                }
            })
            .collect()
    }

    /// Get output names
    fn get_output_names(&self) -> Vec<String> {
        self.graph_info
            .operands
            .iter()
            .filter_map(|op| {
                if matches!(op.kind, crate::graph::OperandKind::Output) {
                    op.name.clone()
                } else {
                    None
                }
            })
            .collect()
    }
}

impl PyMLGraph {
    pub fn new(graph_info: GraphInfo) -> Self {
        Self { graph_info }
    }
}
