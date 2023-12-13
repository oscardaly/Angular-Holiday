const dotenv = require('dotenv');

dotenv.config();

export const environment = {
    production: false,
    api: {
      serverUrl: process.env['API_SERVER_URL'],
    },
    auth0: {
      domain: process.env['AUTH0_DOMAIN'],
      clientId: process.env['AUTH0_CLIENT_ID'],
      authorizationParams: {
        audience: process.env['AUTH0_AUDIENCE'],
        redirect_uri: process.env['AUTH0_CALLBACK_URL'],
      },
      errorPath: '/callback',
    },
  };