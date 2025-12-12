use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

/// 加法运算
#[pyfunction]
fn add(a: f64, b: f64) -> f64 {
    a + b
}

/// 减法运算
#[pyfunction]
fn subtract(a: f64, b: f64) -> f64 {
    a - b
}

/// 乘法运算
#[pyfunction]
fn multiply(a: f64, b: f64) -> f64 {
    a * b
}

/// 除法运算
#[pyfunction]
fn divide(a: f64, b: f64) -> PyResult<f64> {
    if b == 0.0 {
        return Err(PyValueError::new_err("除数不能为零"));
    }
    Ok(a / b)
}

/// 计算幂
#[pyfunction]
fn power(base: f64, exponent: f64) -> f64 {
    base.powf(exponent)
}

/// 反转字符串
#[pyfunction]
fn reverse_string(s: &str) -> String {
    s.chars().rev().collect()
}

/// 将字符串转换为大写
#[pyfunction]
fn to_uppercase(s: &str) -> String {
    s.to_uppercase()
}

/// 将字符串转换为小写
#[pyfunction]
fn to_lowercase(s: &str) -> String {
    s.to_lowercase()
}

/// 统计字符串中的字符数
#[pyfunction]
fn count_chars(s: &str) -> usize {
    s.chars().count()
}

/// 数据处理类
#[pyclass]
struct DataProcessor {
    data: Vec<f64>,
}

#[pymethods]
impl DataProcessor {
    /// 创建新的数据处理器
    #[new]
    fn new(data: Vec<f64>) -> Self {
        DataProcessor { data }
    }

    /// 计算总和
    fn sum(&self) -> f64 {
        self.data.iter().sum()
    }

    /// 计算平均值
    fn average(&self) -> PyResult<f64> {
        if self.data.is_empty() {
            return Err(PyValueError::new_err("数据列表不能为空"));
        }
        Ok(self.sum() / self.data.len() as f64)
    }

    /// 获取最大值
    fn max(&self) -> PyResult<f64> {
        self.data
            .iter()
            .copied()
            .max_by(|a, b| a.partial_cmp(b).unwrap())
            .ok_or_else(|| PyValueError::new_err("数据列表不能为空"))
    }

    /// 获取最小值
    fn min(&self) -> PyResult<f64> {
        self.data
            .iter()
            .copied()
            .min_by(|a, b| a.partial_cmp(b).unwrap())
            .ok_or_else(|| PyValueError::new_err("数据列表不能为空"))
    }

    /// 获取数据数量
    fn count(&self) -> usize {
        self.data.len()
    }

    /// 添加数据
    fn add_data(&mut self, value: f64) {
        self.data.push(value);
    }

    /// 获取所有数据
    fn get_data(&self) -> Vec<f64> {
        self.data.clone()
    }
}

/// Python 模块入口
#[pymodule]
fn __NAME__(_py: Python, m: &PyModule) -> PyResult<()> {
    // 注册数学函数
    m.add_function(wrap_pyfunction!(add, m)?)?;
    m.add_function(wrap_pyfunction!(subtract, m)?)?;
    m.add_function(wrap_pyfunction!(multiply, m)?)?;
    m.add_function(wrap_pyfunction!(divide, m)?)?;
    m.add_function(wrap_pyfunction!(power, m)?)?;
    
    // 注册字符串函数
    m.add_function(wrap_pyfunction!(reverse_string, m)?)?;
    m.add_function(wrap_pyfunction!(to_uppercase, m)?)?;
    m.add_function(wrap_pyfunction!(to_lowercase, m)?)?;
    m.add_function(wrap_pyfunction!(count_chars, m)?)?;
    
    // 注册类
    m.add_class::<DataProcessor>()?;
    
    Ok(())
}

