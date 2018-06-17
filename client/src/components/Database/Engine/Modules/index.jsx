import React from 'react'
import axios from 'axios'
import Config from '../../../Config'

const SERVER_ADDR = Config();

class EngineModules extends React.Component{

    static moduleList(){
        return axios.get(SERVER_ADDR + '/module/all').then(res => {
            return res.data;
        })
    }

    static moduleSearch(moduleImport){
        return axios.get(SERVER_ADDR + '/module/' + moduleImport).then(res => {
            return res.data;
        })
    }

    static moduleExecute(moduleImport, moduleArgument){
        const userToken = localStorage.getItem('operativeAuthToken');
        return axios.post(SERVER_ADDR + '/module/use/' + moduleImport + "/" + userToken, moduleArgument)
            .then(res => {
               if(res.data.status !== undefined){
                   if(res.data.status === "success"){
                       if(res.data.task_id !== undefined){
                           return res.data.task_id;
                       }
                   }
                   else if(res.data.status === "forbidden"){
                       return res.data
                   }
               }
            });
    }


    static moduleExecuteProject(module_import, module_argument, project_id, project_subject){
        const userToken = localStorage.getItem('operativeAuthToken');
        const userApp = localStorage.getItem('operativeApp');
        return axios.post(SERVER_ADDR + '/project/run/module', {
            'u_auth_token': userToken,
            'u_app_id': userApp,
            'module_import': module_import,
            'module_argument': module_argument,
            'project_id': project_id,
            'project_subject': project_subject,
        })
            .then(res => {
                return res.data
            })
    }

    render(){
        return(true)
    }
}

export default EngineModules

