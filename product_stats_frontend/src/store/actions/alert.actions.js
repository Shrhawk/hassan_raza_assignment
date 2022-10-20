import { alertConstants } from "../constants/alert.constants";

export const alertActions = {
  success,
  error,
  clear,
  updatedSuccess,
  fileSuccess,
};

function fileSuccess(message) {
  return { type: alertConstants.UPDATED_SUCCESS, message };
}

function updatedSuccess(message) {
  return { type: alertConstants.UPDATED_SUCCESS, message };
}

function success(message) {
  return { type: alertConstants.SUCCESS, message };
}

function error(message) {
  return { type: alertConstants.ERROR, message };
}

function clear() {
  return { type: alertConstants.CLEAR };
}
