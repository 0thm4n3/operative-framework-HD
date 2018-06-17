import axios from 'axios'

const authMiddleware = () => {
    if(localStorage.getItem('operativeAuthToken') === null)
    {
        return false;
    }
    if(localStorage.getItem('operativeApp') === null){
        return false;
    }
    let operativeToken = localStorage.getItem('operativeAuthToken');
    let operativeApp = localStorage.getItem('operativeApp');
    return axios.get('http://127.0.0.1:5000/auth/check/' + operativeToken + "/" + operativeApp)
        .then(res => {
            if(res.data.status === "forbidden"){
                return false;
            }
            else if(res.data.status === "success"){
                return true;
            }
        });
};

export default authMiddleware;