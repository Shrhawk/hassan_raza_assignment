import API from '../../api/auth';
import { authConstants } from '../constants/auth.constants';
import { alertActions } from './alert.actions';
import axios from 'axios';

export const authActions = {
    login,
    getProfile,
    logout,
    getCountries,
    getCities,
    uploadCSVFile,
    uploadUserProfile,
    getUserSale,
    getSaleGraph
};

const Url = 'https://product-stats-backend-api.herokuapp.com';

function login(email, password) {
    return (dispatch) => {
        dispatch(request(email));
        return API(
            `${Url}/api/user_login`,
            { email, password },
            'post',
            false,
            true
        )
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    localStorage.setItem(
                        'accessToken',
                        `${user.data.data.access_token}`
                    );
                    localStorage.setItem(
                        'refreshToken',
                        `${user.data.data.refresh_token}`
                    );

                    dispatch(alertActions.success('Login successful'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function request(user) {
        return { type: authConstants.LOGIN_REQUEST, user };
    }
    function success(user) {
        return { type: authConstants.LOGIN_SUCCESS, user };
    }
    
}

function getProfile() {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };

    return (dispatch) => {
        return axios
            .get(`${Url}/api/get_profile`, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(alertActions.success('get profile successfully'));
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.USER_PROFILE_SUCCESS, user };
    }
}

function logout() {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .post(
                `${Url}/api/user_logout`,
                { refresh_token: localStorage.getItem('refreshToken') },
                config
            )
            .then(
                (user) => {
                    dispatch(
                        success({
                            success: true,
                            message: 'User logout successfully'
                        })
                    );
                    dispatch(alertActions.success('Logout successful'));
                    localStorage.removeItem('accessToken');
                    localStorage.removeItem('refreshToken');
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.LOGOUT_SUCCESS, user };
    }
}

function getCountries() {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };

    return (dispatch) => {
        return axios
            .get(`${Url}/api/countries`, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(alertActions.success('Login successful'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.COUNTRIES_SUCCESS, user };
    }
}

function getCities(id) {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .get(`${Url}/api/city?country_id=${id}`, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(alertActions.success('Login successful'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 1000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.CITIES_SUCCESS, user };
    }
}

function uploadCSVFile(data) {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .post(`${Url}/api/upload_sale_data`, data, config)
            .then(
                (user) => {
                    dispatch(success(user.data));
                    dispatch(
                        alertActions.fileSuccess('File updated successfully')
                    );
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.FILE_UPLOAD_SUCCESS, user };
    }
}

function uploadUserProfile(data) {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .put(`${Url}/api/update_profile`, data, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(
                        alertActions.success('profile successfully updated')
                    );
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.UPDATE_USER_PROFILE_SUCCESS, user };
    }
}

function getUserSale() {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .get(`${Url}/api/user_sale_data`, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(
                        alertActions.success('successfully get user sale data')
                    );
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.USER_SALE_DATA, user };
    }
}

function getSaleGraph() {
    const config = {
        headers: {
            Authorization: `Bearer ${localStorage.getItem('accessToken')}`
        }
    };
    return (dispatch) => {
        return axios
            .get(`${Url}/api/graph_sale_data`, config)
            .then(
                (user) => {
                    dispatch(success(user.data.data));
                    dispatch(
                        alertActions.success('successfully get graph sale data')
                    );
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                },
                (error) => {
                    dispatch(alertActions.error('Something went wrong'));
                    setTimeout(() => {
                        dispatch(alertActions.clear());
                    }, 2000);
                }
            )
            .catch(() => {
                dispatch(alertActions.error('Something went wrong'));
                setTimeout(() => {
                    dispatch(alertActions.clear());
                }, 2000);
            });
    };

    function success(user) {
        return { type: authConstants.GRAPH_SALE_SUCCESS, user };
    }
}
