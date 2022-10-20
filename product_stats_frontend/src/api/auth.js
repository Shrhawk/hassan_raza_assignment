import RequestInstance from "../utils/httpHelpers";


export default function(route, data, requestType, includeBasicAuth = false, includeJwtToken = false ){
    var request_instance = RequestInstance({
        includeBasicAuth: includeBasicAuth,
        includeJwtToken: includeJwtToken,
    });

    switch (requestType) {
        case 'post':
            return request_instance.post(
                route,
                data
            );            
        case 'put':
            return request_instance.put(
                route,
                data
            );            
    
        default:
            return request_instance.get(
                '*'
            );            
    }


}