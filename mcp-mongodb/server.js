import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { MongoClient } from "mongodb";
import { z } from "zod";
import "dotenv/config";

const MONGODB_URI = process.env.MONGODB_URI || "mongodb://localhost:27017";

let client = null;

async function getClient() {
  if (!client) {
    client = new MongoClient(MONGODB_URI);
    await client.connect();
  }
  return client;
}

const server = new McpServer({
  name: "mcp-mongodb",
  version: "1.0.0",
});

// Listar bancos de dados
server.tool(
  "list_databases",
  "Lista todos os bancos de dados disponíveis",
  {},
  async () => {
    const c = await getClient();
    const result = await c.db().admin().listDatabases();
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result.databases, null, 2),
        },
      ],
    };
  }
);

// Listar coleções
server.tool(
  "list_collections",
  "Lista todas as coleções de um banco de dados",
  {
    database: z.string().describe("Nome do banco de dados"),
  },
  async ({ database }) => {
    const c = await getClient();
    const collections = await c.db(database).listCollections().toArray();
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(collections, null, 2),
        },
      ],
    };
  }
);

// Buscar documentos
server.tool(
  "find",
  "Busca documentos em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().optional().describe("Filtro em JSON (ex: {\"nome\": \"João\"})"),
    limit: z.number().optional().describe("Número máximo de documentos (padrão: 20)"),
    skip: z.number().optional().describe("Documentos a pular (paginação)"),
  },
  async ({ database, collection, filter, limit, skip }) => {
    const c = await getClient();
    const filterObj = filter ? JSON.parse(filter) : {};
    const docs = await c
      .db(database)
      .collection(collection)
      .find(filterObj)
      .skip(skip ?? 0)
      .limit(limit ?? 20)
      .toArray();
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(docs, null, 2),
        },
      ],
    };
  }
);

// Contar documentos
server.tool(
  "count_documents",
  "Conta documentos em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().optional().describe("Filtro em JSON"),
  },
  async ({ database, collection, filter }) => {
    const c = await getClient();
    const filterObj = filter ? JSON.parse(filter) : {};
    const count = await c.db(database).collection(collection).countDocuments(filterObj);
    return {
      content: [
        {
          type: "text",
          text: `Total de documentos: ${count}`,
        },
      ],
    };
  }
);

// Inserir um documento
server.tool(
  "insert_one",
  "Insere um único documento em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    document: z.string().describe("Documento em JSON a ser inserido"),
  },
  async ({ database, collection, document }) => {
    const c = await getClient();
    const doc = JSON.parse(document);
    const result = await c.db(database).collection(collection).insertOne(doc);
    return {
      content: [
        {
          type: "text",
          text: `Documento inserido com _id: ${result.insertedId}`,
        },
      ],
    };
  }
);

// Inserir múltiplos documentos
server.tool(
  "insert_many",
  "Insere múltiplos documentos em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    documents: z.string().describe("Array de documentos em JSON"),
  },
  async ({ database, collection, documents }) => {
    const c = await getClient();
    const docs = JSON.parse(documents);
    const result = await c.db(database).collection(collection).insertMany(docs);
    return {
      content: [
        {
          type: "text",
          text: `${result.insertedCount} documentos inseridos. IDs: ${JSON.stringify(Object.values(result.insertedIds))}`,
        },
      ],
    };
  }
);

// Atualizar um documento
server.tool(
  "update_one",
  "Atualiza o primeiro documento que corresponde ao filtro",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().describe("Filtro em JSON para encontrar o documento"),
    update: z.string().describe("Operação de atualização em JSON (ex: {\"$set\": {\"nome\": \"Maria\"}})"),
    upsert: z.boolean().optional().describe("Criar documento se não existir (padrão: false)"),
  },
  async ({ database, collection, filter, update, upsert }) => {
    const c = await getClient();
    const result = await c
      .db(database)
      .collection(collection)
      .updateOne(JSON.parse(filter), JSON.parse(update), { upsert: upsert ?? false });
    return {
      content: [
        {
          type: "text",
          text: `Documentos encontrados: ${result.matchedCount}, modificados: ${result.modifiedCount}${result.upsertedId ? `, inserido com _id: ${result.upsertedId}` : ""}`,
        },
      ],
    };
  }
);

// Atualizar múltiplos documentos
server.tool(
  "update_many",
  "Atualiza todos os documentos que correspondem ao filtro",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().describe("Filtro em JSON"),
    update: z.string().describe("Operação de atualização em JSON"),
  },
  async ({ database, collection, filter, update }) => {
    const c = await getClient();
    const result = await c
      .db(database)
      .collection(collection)
      .updateMany(JSON.parse(filter), JSON.parse(update));
    return {
      content: [
        {
          type: "text",
          text: `Documentos encontrados: ${result.matchedCount}, modificados: ${result.modifiedCount}`,
        },
      ],
    };
  }
);

// Deletar um documento
server.tool(
  "delete_one",
  "Deleta o primeiro documento que corresponde ao filtro",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().describe("Filtro em JSON"),
  },
  async ({ database, collection, filter }) => {
    const c = await getClient();
    const result = await c
      .db(database)
      .collection(collection)
      .deleteOne(JSON.parse(filter));
    return {
      content: [
        {
          type: "text",
          text: `Documentos deletados: ${result.deletedCount}`,
        },
      ],
    };
  }
);

// Deletar múltiplos documentos
server.tool(
  "delete_many",
  "Deleta todos os documentos que correspondem ao filtro",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    filter: z.string().describe("Filtro em JSON"),
  },
  async ({ database, collection, filter }) => {
    const c = await getClient();
    const result = await c
      .db(database)
      .collection(collection)
      .deleteMany(JSON.parse(filter));
    return {
      content: [
        {
          type: "text",
          text: `Documentos deletados: ${result.deletedCount}`,
        },
      ],
    };
  }
);

// Aggregation pipeline
server.tool(
  "aggregate",
  "Executa um pipeline de agregação em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    pipeline: z.string().describe("Pipeline de agregação em JSON (array de estágios)"),
  },
  async ({ database, collection, pipeline }) => {
    const c = await getClient();
    const result = await c
      .db(database)
      .collection(collection)
      .aggregate(JSON.parse(pipeline))
      .toArray();
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }
);

// Criar índice
server.tool(
  "create_index",
  "Cria um índice em uma coleção",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção"),
    keys: z.string().describe("Campos do índice em JSON (ex: {\"nome\": 1, \"idade\": -1})"),
    unique: z.boolean().optional().describe("Se o índice deve ser único (padrão: false)"),
  },
  async ({ database, collection, keys, unique }) => {
    const c = await getClient();
    const name = await c
      .db(database)
      .collection(collection)
      .createIndex(JSON.parse(keys), { unique: unique ?? false });
    return {
      content: [
        {
          type: "text",
          text: `Índice criado: ${name}`,
        },
      ],
    };
  }
);

// Criar coleção
server.tool(
  "create_collection",
  "Cria uma nova coleção em um banco de dados",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção a ser criada"),
  },
  async ({ database, collection }) => {
    const c = await getClient();
    await c.db(database).createCollection(collection);
    return {
      content: [
        {
          type: "text",
          text: `Coleção '${collection}' criada no banco '${database}'`,
        },
      ],
    };
  }
);

// Dropar coleção
server.tool(
  "drop_collection",
  "Remove uma coleção e todos os seus documentos",
  {
    database: z.string().describe("Nome do banco de dados"),
    collection: z.string().describe("Nome da coleção a ser removida"),
  },
  async ({ database, collection }) => {
    const c = await getClient();
    const dropped = await c.db(database).collection(collection).drop();
    return {
      content: [
        {
          type: "text",
          text: dropped
            ? `Coleção '${collection}' removida com sucesso`
            : `Coleção '${collection}' não encontrada`,
        },
      ],
    };
  }
);

// Iniciar servidor
const transport = new StdioServerTransport();
await server.connect(transport);

process.on("SIGINT", async () => {
  if (client) await client.close();
  process.exit(0);
});
