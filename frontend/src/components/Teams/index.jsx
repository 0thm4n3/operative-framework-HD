import React from 'react'
import EngineUsers from '../Database/Engine/Users'
import styled from 'styled-components'
import {Link} from 'react-router-dom'
import Message from '../Message'

const tableTeam = {
    background: "#fafafa",
    borderRadius: "0 !important",
    boxShadow: "0 0 0 0",
};

const Screen = styled.div`
        .buttonBasic{
            box-shadow: 0 0 0 0 !important;
            border-bottom: 3px solid #e77d03;
            border-left: 1px solid #ffffff !important;
            border-radius: 0 !important;
            background: #fafafa !important;
            color: #4e2b01 !important;
        }
        .formArgument{
            border-radius: 0 0 0 0;
            background-color: #b1b1b121 !important;
            
        }
`;

class Teams extends React.Component{

    constructor(){
        super();
        this.state = {
            'teams': [],
            'userMessage':'',
            'userStatus':''
        };

        EngineUsers.getTeams()
            .then(res => {
                if(res.status === "success"){
                    this.setState({
                        'teams': res.teams,
                    })
                }
            });

        this.deleteUser = this.deleteUser.bind(this);
    }


    deleteUser(e){
        let teams = this.state.teams;
        let username = e.target.dataset.user;
        let u_key = undefined;
        if(e.target.dataset.key !== undefined){
            u_key = e.target.dataset.key
        }
        EngineUsers.deleteTeamMember(username).then(res => {
            if(res.msg !== undefined && res.status !== undefined){
                if(res.status === "forbidden"){
                    this.setState({
                        'userMessage': res.msg,
                        'userStatus': 'negative'
                    })
                }
                else if(res.status === "success"){
                    if(u_key !== undefined){
                        delete teams[u_key]
                    }
                    this.setState({
                        'userMessage': res.msg,
                        'userStatus': 'positive',
                        'teams': teams
                    });
                }
            }
        })
    }

    userListing(){
        const rows = [];
        this.state.teams.forEach((value, i) => {
            rows.push(
                <tr key={i}>
                    <td>{value.username}</td>
                    <td>{value.user_right}</td>
                    <td><button className={"ui button mini buttonBasic basic"}><i onClick={this.deleteUser} data-key={i} data-user={value.username} className="fas fa-trash-alt"></i></button></td>
                </tr>
            )
        });
        return rows;
    }

    render(){
        return (

            <Screen>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                    <Link to="/teams/add" className="ui button basic mini buttonBasic">
                        <i className="fas fa-plus"></i>
                    </Link>
                <table className="ui basic table orange">
                    <thead style={tableTeam}>
                    </thead>
                    <tbody>
                    {this.userListing()}
                    </tbody>
                </table>
            </Screen>
        )
    }

}

export class AddMember extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            'username': '',
            'password': '',
            'repassword': '',
            'user_right': 'Viewer',
            'userMessage': '',
            'userStatus': ''
        };

        this.setUsername = this.setUsername.bind(this);
        this.setPassword = this.setPassword.bind(this);
        this.setRePassword = this.setRePassword.bind(this);
        this.registerUser = this.registerUser.bind(this);
        this.setRight = this.setRight.bind(this);
    }

    setUsername(e){
        this.setState({
            'username': e.target.value
        });
    }

    setPassword(e){
        this.setState({
           'password': e.target.value
        });
    }

    setRePassword(e){
        this.setState({
            'repassword': e.target.value
        })
    }

    setRight(e){
        this.setState({
            'user_right': e.target.value
        })
    }

    registerUser(){
        let element = document.getElementById('addTeam');
        element.classList.add("loading");
        EngineUsers.addTeamMember(this.state.username, this.state.password, this.state.repassword, this.state.user_right)
            .then(res => {
                if(res.status !== undefined && res.msg !== undefined){
                    if(res.status === "forbidden"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'negative'
                        })
                    }
                    else if(res.status === "success"){
                        this.setState({
                            'userMessage': res.msg,
                            'userStatus': 'positive'
                        })
                    }
                }
                element.classList.remove("loading");
            })
    }

    render(){
        return(
            <Screen>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userStatus}/>
                <Link to={"/teams"} className={""}>Go to teams</Link>
                <div className={"ui segment formArgument"}>
                    <div className={"ui form"}>
                        <div className={"field"}>
                            <label>Username</label>
                            <input type={"text"} placeholder={"teamMember1"} onChange={this.setUsername} />
                        </div>
                        <div className={"field"}>
                            <label>Password</label>
                            <input type={"password"} placeholder={"Y0uRp4$$0rD"} onChange={this.setPassword}/>
                        </div>
                        <div className={"field"}>
                            <label>Re-Password</label>
                            <input type={"password"} placeholder={"Y0uRp4$$0rD"} onChange={this.setRePassword}/>
                        </div>
                        <div className={"field"}>
                            <label>User right</label>
                            <select className={"ui fluid dropdown"} onChange={this.setRight}>
                                <option value="Viewer">Viewer</option>
                                <option value="Contributor">Contributor</option>
                                <option value="Administrator">Administrator</option>
                            </select>
                        </div>
                    </div>
                </div>
                <button id={"addTeam"} className={"ui button basic mini buttonBasic"} onClick={this.registerUser}>Add a Member</button>
            </Screen>
        )
    }
}

export default Teams