use astroxide::regions::{SphericalAnulus, SphericalAperture, SphericalPolygon};
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

#[pymodule]
fn regionx(m: &Bound<'_, PyModule>) -> PyResult<()> {
    // Add your functions here
    m.add_class::<Polygon>()?;
    m.add_class::<Anulus>()?;
    m.add_class::<Aperture>()?;
    Ok(())
}
