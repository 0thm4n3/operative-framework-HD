import React from 'react'
import EngineModules from '../Database/Engine/Modules/index'
import {Link} from 'react-router-dom'
import styled from 'styled-components'
import Message from '../Message'

const divTitle = {
    'color': '#e67e00',
    'fontSize': '1.1em',
    'fontWeight': '800',
    'textTransform': 'uppercase',
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
        .requiredInput{
            color: orange !important;
            text-transform: none;
        }
`;

const divElement = {
    'fontSize': '1em',
    'fontWeight': '800',
};

const divTitleModule = {
    'textTransform': 'capitalize',
};


const divInput = {
    'borderBottom': '4px solid #e67e00',
    'borderRadius': '0 0 0 0 !important',
};

class Module extends React.Component{

    constructor(){
        super();
        this.state = {
            modulesList:[]
        };

        EngineModules.moduleList().then(res => {
            this.setState({
                modulesList: res.modules,
            })
        })
    }

    moduleListing(){
        const rows = [];
        this.state.modulesList.forEach((module, i) => {
            rows.push(
                <tr key={i}>
                    <td>{module.module_import}</td>
                    <td>{module.module_name}</td>
                    <td>{module.module_description}</td>
                    <td><Link to={"/m/info/"+module.module_import}><i className={"fas fa-sync"}></i> execute</Link></td>
                </tr>
            )
        });
        return rows
    }

    render(){
        return(
            <div>
            <table className="ui basic table orange">
                <thead>
                <tr>
                    <th>ID</th>
                    <th>Module</th>
                    <th>Description</th>
                    <th></th>
                </tr>
                </thead>
                <tbody>
                {this.moduleListing()}

                </tbody>
            </table>
            </div>
        )
    }
}

export class UseModule extends React.Component{

    constructor(props){
        super(props);
        this.state = {
            moduleImport: this.props.match.params.moduleImport,
            moduleInformation: [],
            moduleArguments: [],
            moduleStatus: "",
            moduleFound: "",
            userMessage: "",
            userMessageStatus: "",
        };
        this.setArgument = this.setArgument.bind(this);
        this.checkArgument = this.checkArgument.bind(this);
        this.executeModule = this.executeModule.bind(this);
        this.loadModule();
    }

    setArgument(e){
        let argumentName = e.target.getAttribute('data-argument');
        let argumentValue = e.target.value;
        if(argumentName !== null && argumentValue !== null) {
            this.state.moduleArguments.forEach((argument, index) => {
                if (argument.name === argumentName) {
                    let item = this.state.moduleArguments[index];
                    item.value = argumentValue;
                    this.setState({item});
                }
            })
        }
    }

    checkArgument(){
        let ret = true;
        if(this.state.moduleArguments.length < 1)
        {
            return ret;
        }
        this.state.moduleArguments.forEach((argument, index) => {
            if(argument.required === "yes" && argument.value === "") {
                ret =  false
            }
        });
        return ret
    }

    executeModule(){
        let check = this.checkArgument();
        if(check){
            let tpl_arguments = {};
            this.state.moduleArguments.forEach((argument, index) => {
                if(tpl_arguments.hasOwnProperty(argument.name) === false){
                    tpl_arguments[argument.name] = argument.value;
                }
            });
            EngineModules.moduleExecute(this.state.moduleImport, tpl_arguments).then(execute => {
                if(execute !== false){
                    this.setState({
                        userMessage: "Task as been started with id '"+execute+"'",
                        userMessageStatus: "positive"
                    });
                }
                else{
                    this.setState({
                        userMessage: "A error as been found, please try again later or contact support.",
                        userMessageStatus: "negative"
                    });
                }
            });
        }
        else{
            this.setState({
                userMessage: "Please enter required argument",
                userMessageStatus: "negative"
            })
        }
    }

    loadModule(){
        EngineModules.moduleSearch(this.state.moduleImport).then(res => {
            if(res.status !== undefined && res.module_found === true) {
                this.setState({
                    moduleInformation: res.module_informations[0],
                    moduleArguments: res.module_arguments,
                    moduleStatus: res.status,
                    moduleFound: res.module_found,
                });
            }
            else{
                this.setState({
                    moduleFound: false,
                })
            }
        }).catch(error => {
            this.setState({
                moduleFound: false,
            })
        })
    }

    parseArguments(){
        let rows = [];
        if(this.state.moduleArguments.length < 1)
        {
            return(
                <div>
                    <h5 className="ui horizontal header divider">No arguments</h5>
                    <button className={"ui button right orange buttonBasic"} onClick={this.executeModule}>Execute</button>
                </div>
            )
        }
        this.state.moduleArguments.forEach((argument, index) => {
            let argumentRequired = "";
            if(argument.required === "yes"){
                argumentRequired = "<- required"
            }
            rows.push(
                <div key={index} className={"field"}>
                    <label style={divTitleModule}>{argument.name} <span className={"requiredInput"}>{argumentRequired}</span></label>
                    <input style={divInput} data-argument={argument.name} type={"text"} placeholder={argument.placeholder} onChange={this.setArgument}/>
                </div>
            );
        });
        return (
            <div>
                <h5 className="ui horizontal header divider">Module arguments</h5>
                <div className={"ui form segment formArgument"}>{rows}</div>
                <button className={"ui button right orange buttonBasic"} onClick={this.executeModule}>Execute</button>
            </div>);
    }

    render(){
        if(this.state.moduleFound === false)
        {
            return(
                <div className={"ui segment"}>
                    <Message userStatus={"negative"} userMessage={"Module not found or not migrated to sass version."}/>
                    <Link to={"/modules"}>Back to modules listing?</Link>
                </div>
            )
        }
        return(
            <Screen className={"ui segment"}>
                <Message userMessage={this.state.userMessage} userStatus={this.state.userMessageStatus}/>
                <table className="ui very basic table">
                    <thead>
                    </thead>
                    <tbody>
                    <tr>
                        <td style={divTitle}><b>Name</b></td>
                        <td style={divElement}>{this.state.moduleInformation.module_name}</td>
                    </tr>
                    <tr>
                        <td style={divTitle}><b>Description</b></td>
                        <td style={divElement}>{this.state.moduleInformation.module_description}</td>
                    </tr>
                    <tr>
                        <td style={divTitle}><b>Alias</b></td>
                        <td style={divElement}>{this.state.moduleInformation.module_import}</td>
                    </tr>
                    </tbody>
                </table>
                {this.parseArguments()}
            </Screen>
        )
    }
}

export default Module