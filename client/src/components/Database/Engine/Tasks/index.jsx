import React from 'react'
import axios from 'axios'
import Config from '../../../Config'


const SERVER_ADDR = Config();

class EngineTasks extends React.Component{

    static getAll(){
        let operativeToken = localStorage.getItem('operativeAuthToken');
        return axios.get(SERVER_ADDR + '/view/task/' + operativeToken)
            .then(res => {
               if(res.data.status !== undefined){
                   return res.data;
               }
               return {
                   'status': 'forbidden'
               }
            });
    }

    static getTask(taskId){
        let operativeToken = localStorage.getItem('operativeAuthToken');
        return axios.get(SERVER_ADDR + '/view.task/'+taskId+'/' + operativeToken)
            .then(res => {
                if(res.data.status !== undefined && res.data.status !== 'forbidden'){
                    return res.data
                }
                else {
                    return {
                        'status': 'forbidden'
                    }
                }
            })
    }
}

export default EngineTasks