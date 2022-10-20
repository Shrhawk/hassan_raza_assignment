import axios from 'axios';
import store from '../store';
import constants from './constants';

const BASE_URL = constants.ApiPath + constants.apiPrefix;



export function RequestInstance({
    includeBasicAuth = false,
    includeJwtToken = true,
    fileUploading = false
}) {
    const state = store.getState();
    
    let UserLoggedIn = false;
    
    const Instance = axios.create({
        baseURL: BASE_URL,
        timeout: 10000,
        validateStatus: function (status) {
            return status < 500; // Resolve only if the status code is less than 500
        }
    });

    state.auth?.user?.access_token ? (UserLoggedIn = true) : (UserLoggedIn = false);
    if (includeJwtToken === true) {
        if (UserLoggedIn === true) {
            Instance.defaults.headers.common['Authorization'] =
                'Bearer ' + state.auth?.user?.access_token;
        }
    }
    if (fileUploading === true) {
        Instance.defaults.headers.post['Content-Type'] = 'multipart/form-data';
    }

    Instance.interceptors.response.use(
        (res) => {
            if (res.status === 401) {
                // store.store.dispatch(logout());
            }
            return res;
        },
        (err) => {
            return Promise.reject(err);
        }
    );
    return Instance;
}

export default RequestInstance;
