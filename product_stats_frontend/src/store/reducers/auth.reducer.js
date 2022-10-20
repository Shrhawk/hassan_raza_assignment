import { authConstants } from '../constants/auth.constants';

const initialState = {
    user: [],
    userProfile: {},
    countries: [],
    cities: [],
    fileUploadsuccess: [],
    userSaleData: [],
    graphSaleData: []
};

export function auth(state = initialState, action) {
    switch (action.type) {
        case authConstants.LOGIN_REQUEST:
            return {
                loggingIn: true,
                user: action.user
            };
        case authConstants.LOGIN_SUCCESS:
            return {
                loggedIn: true,
                user: action.user
            };
        case authConstants.REGISTER_SUCCESS:
            return {
                user: action.user
            };
        case authConstants.USER_PROFILE_SUCCESS:
            return {
                ...state,
                userProfile: action.user
            };
        case authConstants.COUNTRIES_SUCCESS:
            return {
                ...state,
                countries: action.user
            };
        case authConstants.CITIES_SUCCESS:
            return {
                ...state,
                cities: action.user
            };
        case authConstants.REGISTER_FAILURE:
            return {};
        case authConstants.LOGIN_FAILURE:
            return {};
        case authConstants.LOGOUT_SUCCESS:
            return {
                user: action.user
            };
        case authConstants.FILE_UPLOAD_SUCCESS:
            return {
                ...state,
                fileUploadsuccess: action.user
            };
        case authConstants.USER_SALE_DATA:
            return {
                ...state,
                userSaleData: action.user
            };
        case authConstants.GRAPH_SALE_SUCCESS:
            return {
                ...state,
                graphSaleData: action.user
            };
        default:
            return state;
    }
}
