import api from "./api";

export const getLocations = async () => {
  const response = await api.get("/locations/");
  return response.data;
};

export const getLocation = async (locationId) => {
  const response = await api.get(`/locations/${locationId}`);
  return response.data;
};