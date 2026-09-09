import api from "./api";


export const getHospitals = async () => {
  const response = await api.get("/hospitals/");
  return response.data;
};


export const getHospital = async (hospitalId) => {
  const response = await api.get(`/hospitals/${hospitalId}`);
  return response.data;
};
