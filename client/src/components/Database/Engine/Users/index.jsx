import React from 'react'
import axios from 'axios'
import Config from '../../../Config'

const SERVER_ADDR = Config();

class EngineUsers extends React.Component{

    static personalInformation(){
        let userToken = localStorage.getItem('operativeAuthToken');
        if(userToken === null){
            return(false);
        }
        return axios.get(SERVER_ADDR + '/user/account/' + userToken).then(res => {
            if(res.data.status === "success"){
                return res.data.user;
            }
            else{
                return false;
            }
        });
    }

    static registerUser(){
        console.log('register user');
    }

    static addTeamMember(username, password, repassword, user_right){

        let userToken = localStorage.getItem('operativeAuthToken');
        let userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + "/team/add/member", {
            'u_username': username,
            'u_password': password,
            'u_repassword': repassword,
            'u_app_id': userApp,
            'u_auth_token': userToken,
            'u_right': user_right
        }).then(res => {
            return res.data
        })
    }

    static deleteTeamMember(username){
        let userToken = localStorage.getItem('operativeAuthToken');
        let userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + "/team/delete/member", {
            'u_username': username,
            'u_auth_token': userToken,
            'u_app_id': userApp
        }).then(res => {
            return res.data
        })
    }

    static getTeams(){
        let userToken = localStorage.getItem('operativeAuthToken');
        let userApp = localStorage.getItem('operativeApp');

        return axios.get(SERVER_ADDR + '/user/teams/' + userToken + '/' + userApp)
            .then(res => {
                if(res.data.status === "success"){
                    return res.data;
                }
                else{
                    return false;
                }
            });
    }

}

export default EngineUsers;