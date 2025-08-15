import {
  CopilotRuntime,
  OpenAIAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";
import { NextRequest } from "next/server";
import OpenAI from "openai";

// Create a dummy OpenAI adapter - the actual LLM calls are handled by the remote endpoint
// This is required to satisfy the TypeScript types for CopilotKit
const openai = new OpenAI({
  apiKey: process.env.OPENAI_API_KEY || "dummy-key-for-remote-endpoint"
});
const serviceAdapter = new OpenAIAdapter({ openai });

const runtime = new CopilotRuntime({
  remoteEndpoints: [
    {
      url: "http://localhost:1338/copilotkit",
      // url: "https://run.blaxel.ai/main/agents/AGENT_NAME/copilotkit",
      onBeforeRequest: () => {
        return {
          headers: {
            "X-Blaxel-Authorization":
              "Bearer <API_KEY / TOKEN>",
          },
        };
      },
    },
  ],
});

export const POST = async (req: NextRequest) => {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
};