import React from 'react'
import EngineTasks from '../Database/Engine/Tasks'
import {Link} from 'react-router-dom'

class Tasks extends React.Component{


    constructor(){
        super();
        this.state = {
            'listStatus':'',
            'listTasks': []
        };

        EngineTasks.getAll()
            .then(res => {
                if(res.status === "success") {
                    this.setState({
                        listStatus: res.status,
                        listTasks: res.tasks,
                    });
                }
            });
    }

    printTable(){
        let rows = [];
        this.state.listTasks.forEach((task, index) => {
            console.log(task)
            rows.push(
                <tr key={index}>
                    <td>{task.module_name}</td>
                    <td>{task.task_id}</td>
                    <td>{task.username}</td>
                    <td>{task.status}</td>
                    <td><Link to={"/task/view/" + task.task_id}><i class="far fa-eye"></i> view</Link></td>
                </tr>
            )
        })
        return rows
    }

    render(){
        return(
            <table className="ui basic table orange">
                <thead>
                <tr>
                    <th>Module</th>
                    <th>Task</th>
                    <th>created by</th>
                    <th>Status</th>
                    <th>View</th>
                </tr>
                </thead>
                <tbody>
                {this.printTable()}
                </tbody>
            </table>
        )
    }
}

export class ViewTask extends React.Component{
    constructor(props){
        super(props);
        this.state = {
            loading: <i className="fa fa-spinner fa-pulse fa-3x fa-fw"></i>,
            taskId: this.props.match.params.taskId,
            taskTemplate: [],
            taskTh:[],
            taskResult:[],
            taskTd: [],
            taskKey:[],
        };
        EngineTasks.getTask(this.state.taskId)
            .then(res => {
                if(res.status === 'success') {
                    let thList = [];
                    let taskKey = [];
                    if (res.result.results.length > 0) {
                        let resultat = res.result.results[0];
                        resultat.forEach((result, index) => {
                            if (Object.keys(result).length > 0) {
                                Object.keys(result).forEach((k, i) => {
                                    if (taskKey.indexOf(k) <= -1) {
                                        thList.push(<th key={i}>{k}</th>);
                                        taskKey.push(k)
                                    }
                                })
                            }
                        });
                        this.setState({
                            taskTh: thList,
                            taskResult: resultat,
                            taskKey: taskKey,
                            loading: <i></i>,
                        });
                        if (this.state.taskKey.length > 0) {
                            let taskTd = [];
                            let element = [];
                            this.state.taskResult.forEach((value, index) => {
                                let taskValue = [];
                                this.state.taskKey.forEach((v, i) => {
                                    taskValue.push(<td key={i}>{value[v]}</td>);
                                    element.push(value[v]);
                                });
                                taskTd.push(<tr key={index}>{taskValue}</tr>);
                            });
                            this.setState({taskTd: taskTd})
                        }
                    }
                    else{
                        this.setState({
                            loading: <p>Nothing here.</p>
                        })
                    }
                }
            });
    }

    render(){
        return(
            <div>
                {this.state.loading}
                <table className="ui basic table orange">
                    <thead>
                    <tr>
                        {this.state.taskTh}
                    </tr>
                    </thead>
                    <tbody>
                    {this.state.taskTd}
                    </tbody>
                </table>
            </div>
        )
    }
}

export default Tasks