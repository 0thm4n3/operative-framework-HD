import React from 'react'
import {  Route, Redirect } from "react-router-dom";
import authMiddleware from '../Middleware'

const RouteNoAuth = ({component: Component, ...rest}) => {
    if(localStorage.getItem('operativeAuthToken') !== null && authMiddleware()){
        return <Redirect to="/account"/>
    }
    return <Route exact {...rest} component={Component}/>
};

export default RouteNoAuth