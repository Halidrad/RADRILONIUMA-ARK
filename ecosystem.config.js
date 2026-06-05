module.exports = {
  apps: [
    {
      name: "trianiuma-mcp-core",
      script: "mcp_server/index.js",
      interpreter: "node",
      env: {
        NODE_ENV: "production",
      },
      restart_delay: 5000,
      max_restarts: 10,
    }
  ],
};
