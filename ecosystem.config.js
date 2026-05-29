module.exports = {
  apps: [
    {
      name: "LAM_GATEWAY",
      script: "scripts/lam_gateway.py",
      interpreter: "./venv/bin/python",
      args: "monitor",
      autorestart: true,
      watch: false,
      error_file: "~/.pm2/logs/LAM-GATEWAY-error.log",
      out_file: "~/.pm2/logs/LAM-GATEWAY-out.log"
    },
    {
      name: "VALIDATING_EYE",
      script: "scripts/global/validating_eye.py",
      interpreter: "./venv/bin/python",
      cron_restart: "* * * * *",
      autorestart: false,
      watch: false,
      error_file: "~/.pm2/logs/VALIDATING-EYE-error.log",
      out_file: "~/.pm2/logs/VALIDATING-EYE-out.log"
    },
    {
      name: "LAM_QUEUE_WORKER",
      script: "scripts/lam_gateway.py",
      interpreter: "./venv/bin/python",
      args: "run-queue",
      cron_restart: "*/5 * * * *",
      autorestart: false,
      watch: false,
      error_file: "~/.pm2/logs/LAM-QUEUE-error.log",
      out_file: "~/.pm2/logs/LAM-QUEUE-out.log"
    },
    {
      name: "TRIANIUMA_MCP_BRIDGE",
      script: "mcp_server/index.js",
      interpreter: "node",
      autorestart: true,
      watch: false,
      error_file: "~/.pm2/logs/TRIANIUMA-MCP-error.log",
      out_file: "~/.pm2/logs/TRIANIUMA-MCP-out.log"
    }
  ]
};
