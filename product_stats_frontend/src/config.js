const dev = {
    apiUrl: "https://50c4-180-178-188-144.in.ngrok.io",
  };
  
  const prod = {
    apiUrl: process.env.REACT_APP_API_URL,
  };
  
  const config = {
    // Add common config values here
    MAX_ATTACHMENT_SIZE: 5000000,
    // Default to dev if not set
    ...(process.env.REACT_APP_ENV === "prod" ? prod : dev),
  };
  
  export default config;
  