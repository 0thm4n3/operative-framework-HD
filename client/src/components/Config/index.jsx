const Config = () => {
    let config = {
        'protocol': 'http://',
        'server':'127.0.0.1',
        'port': '5000',
    };
    let webService = config.protocol + config.server + ":" + config.port;
    return webService;
};

export default Config