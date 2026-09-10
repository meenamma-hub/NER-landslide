import api from "./api";

export const getRiskData = async (location) => {
  const response = await api.get(`/risk/${location}`);
  return response.data;
};

export const getRiskOverview = async () => {
  const response = await api.get("/risk/overview");
  return response.data;
};