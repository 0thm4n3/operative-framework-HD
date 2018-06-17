import React from "react";
import { Route, Redirect } from "react-router-dom";
import authMiddleware from '../Middleware'

const RouteAuth = ({component: Component, ...rest}) => {
    if(localStorage.getItem('operativeAuthToken') === null || localStorage.getItem('operativeApp') === null){
        return <Redirect to="/login"/>
    }
    authMiddleware().then(res => {
        if(res === false){
            localStorage.clear();
            return <Redirect to="/login"/>
        }
    });
    return <Route exact {...rest} component={Component}/>
};

export default RouteAuth