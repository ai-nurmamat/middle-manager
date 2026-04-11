#!/usr/bin/env node
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { MCPGateway } from './mcp.js';
import { UniversalExtractor } from './llm.js';

async function runServer() {
  const server = new Server(
    {
      name: 'chronos-mcp',
      version: '0.1.0',
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  const gateway = new MCPGateway();
  
  // Setup extractor if API key is provided
  const apiKey = process.env.MINIMAX_API_KEY;
  if (apiKey) {
    const baseUrl = process.env.MINIMAX_BASE_URL || 'https://api.minimax.chat/v1';
    const model = process.env.MINIMAX_MODEL || 'abab6.5-chat';
    gateway.extractor = new UniversalExtractor(apiKey, baseUrl, model);
  }

  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: 'inject_knowledge',
          description: 'Extract S-P-O-T tuples from unstructured text into the temporal graph.',
          inputSchema: {
            type: 'object',
            properties: {
              text: { type: 'string', description: 'Unstructured text' },
              source_id: { type: 'string', description: 'Unique identifier for the source' },
              publish_date: { type: 'string', description: 'Date in YYYY-MM-DD format' }
            },
            required: ['text', 'source_id', 'publish_date']
          }
        },
        {
          name: 'query_graph',
          description: 'Query the Universal 4D Hypergraph memory.',
          inputSchema: {
            type: 'object',
            properties: {
              subject: { type: 'string', description: 'Filter by Subject (Entity)' },
              predicate: { type: 'string', description: 'Filter by Predicate (Relation/Property)' },
              object: { type: 'string', description: 'Filter by Object (Value/Target Entity)' }
            }
          }
        },
        {
          name: 'trigger_sleep',
          description: 'Trigger cognitive consolidation to self-evolve the graph ontology.',
          inputSchema: {
            type: 'object',
            properties: {}
          }
        }
      ],
    };
  });

  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    if (request.params.name === 'inject_knowledge') {
      if (!gateway.extractor) {
        return {
          content: [{ type: 'text', text: JSON.stringify({ error: 'Extractor not configured. Set MINIMAX_API_KEY.' }) }],
        };
      }
      
      const { text, source_id, publish_date } = request.params.arguments as any;
      const res = await gateway.injectKnowledge(text, source_id, publish_date);
      
      return {
        content: [{ type: 'text', text: JSON.stringify(res) }],
      };
    } 
    else if (request.params.name === 'query_graph') {
      const { subject, predicate, object } = request.params.arguments as any;
      const res = gateway.queryGraph({ subject, predicate, object });
      
      return {
        content: [{ type: 'text', text: JSON.stringify(res, null, 2) }],
      };
    }
    else if (request.params.name === 'trigger_sleep') {
      const res = gateway.triggerSleep();
      
      return {
        content: [{ type: 'text', text: JSON.stringify(res) }],
      };
    }
    
    throw new Error(`Tool not found: ${request.params.name}`);
  });

  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error('Chronos MCP server running on stdio');
}

runServer().catch((error) => {
  console.error('Fatal error in server:', error);
  process.exit(1);
});
