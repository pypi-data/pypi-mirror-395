use astroxide::{
    regions::{SphericalAnulus, SphericalAperture, SphericalPolygon, SphericalShape},
    spherical_trig::build_kd_tree,
};
use pyo3::prelude::*;

#[pyclass]
pub struct Polygon {
    polygon: SphericalPolygon,
}

#[pymethods]
impl Polygon {
    #[new]
    pub fn new(ra_verticies: Vec<f64>, dec_verticies: Vec<f64>) -> Self {
        let polygon = SphericalPolygon::new(ra_verticies, dec_verticies);
        Polygon { polygon }
    }

    pub fn is_inside(&self, ra_point: f64, dec_point: f64) -> bool {
        self.polygon.is_inside(ra_point, dec_point)
    }

    pub fn check_points(&self, ra_points: Vec<f64>, dec_points: Vec<f64>) -> Vec<bool> {
        self.polygon.are_inside(&ra_points, &dec_points)
    }
}

#[pyclass]
pub struct Aperture {
    aperture: SphericalAperture,
}

#[pymethods]
impl Aperture {
    #[new]
    pub fn new(ra_center: f64, dec_center: f64, radius_deg: f64) -> Self {
        let sph_app = SphericalAperture::new(ra_center, dec_center, radius_deg);
        Aperture { aperture: sph_app }
    }

    pub fn is_inside(&self, ra_point: f64, dec_point: f64) -> bool {
        self.aperture.is_inside(ra_point, dec_point)
    }

    pub fn check_points(&self, ra_points: Vec<f64>, dec_points: Vec<f64>) -> Vec<bool> {
        self.aperture.are_inside(&ra_points, &dec_points)
    }
}

#[pyclass]
pub struct Anulus {
    anulus: SphericalAnulus,
}

#[pymethods]
impl Anulus {
    #[new]
    pub fn new(ra_center: f64, dec_center: f64, inner_radius: f64, outer_radius: f64) -> Self {
        let sph_app = SphericalAnulus::new(ra_center, dec_center, inner_radius, outer_radius);
        Anulus { anulus: sph_app }
    }

    pub fn is_inside(&self, ra_point: f64, dec_point: f64) -> bool {
        self.anulus.is_inside(ra_point, dec_point)
    }

    pub fn check_points(&self, ra_points: Vec<f64>, dec_points: Vec<f64>) -> Vec<bool> {
        self.anulus.are_inside(&ra_points, &dec_points)
    }
}

#[pyfunction]
pub fn apply_apertures(
    py: Python,
    ras: Vec<f64>,
    decs: Vec<f64>,
    apertures: Vec<Py<Aperture>>,
) -> PyResult<Vec<bool>> {
    let tree = build_kd_tree(&ras, &decs);

    let mut result = vec![false; ras.len()];

    for aperture_py in apertures.iter() {
        let aperture = aperture_py.borrow(py);
        let inside = aperture.aperture.are_inside_tree(&tree, &ras, &decs);

        // Combine with OR logic (like combine_bool_vecs)
        for (r, &ins) in result.iter_mut().zip(inside.iter()) {
            *r = *r || ins;
        }
    }

    Ok(result)
}

#[pyfunction]
pub fn apply_annuli(
    py: Python,
    ras: Vec<f64>,
    decs: Vec<f64>,
    annuli: Vec<Py<Anulus>>,
) -> PyResult<Vec<bool>> {
    let tree = build_kd_tree(&ras, &decs);

    let mut result = vec![false; ras.len()];

    for anulus_py in annuli.iter() {
        let anulus = anulus_py.borrow(py);
        let inside = anulus.anulus.are_inside_tree(&tree, &ras, &decs);

        // Combine with OR logic (like combine_bool_vecs)
        for (r, &ins) in result.iter_mut().zip(inside.iter()) {
            *r = *r || ins;
        }
    }

    Ok(result)
}

#[pyfunction]
pub fn apply_polygons(
    py: Python,
    ras: Vec<f64>,
    decs: Vec<f64>,
    polygons: Vec<Py<Polygon>>,
) -> PyResult<Vec<bool>> {
    let tree = build_kd_tree(&ras, &decs);

    let mut result = vec![false; ras.len()];

    for polygon_py in polygons.iter() {
        let polygon = polygon_py.borrow(py);
        let inside = polygon.polygon.are_inside_tree(&tree, &ras, &decs);

        // Combine with OR logic (like combine_bool_vecs)
        for (r, &ins) in result.iter_mut().zip(inside.iter()) {
            *r = *r || ins;
        }
    }

    Ok(result)
}

#[pymodule]
fn regionx(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add your functions here
    m.add_class::<Polygon>()?;
    m.add_class::<Anulus>()?;
    m.add_class::<Aperture>()?;
    m.add_function(wrap_pyfunction!(apply_apertures, m)?)?;
    m.add_function(wrap_pyfunction!(apply_annuli, m)?)?;
    m.add_function(wrap_pyfunction!(apply_polygons, m)?)?;
    Ok(())
}
