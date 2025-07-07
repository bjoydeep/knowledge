# dependency graphs

### Follow the steps in order

- start the neo4j db
    ```
    podman run \
        --restart always \
        --publish=7474:7474 --publish=7687:7687 \
        --env NEO4J_AUTH=neo4j/neoadmin \
        -e NEO4J_PLUGINS=\[\"apoc\"\] \
        neo4j:2025.01.0
    ```
    - Log into http://localhost:7474/browser as neo4j/neoadmin
    - Paste this [cypher](./cypher/cypher-osdfm.md) and run.
    - The database will be populated.
    - Run `match(p) return(p)` to verify.
    - Here are sample [cypher queries](./cypher/sample_cypher.md) which will allow to explore the graph.
    - Any large LLMs (Gemini et al) are good at generating cypher queries.



#### If you just want to work with dependency graph, you can stop here.
- If you want to inspect the graph using a AI agent, keep going

- create a venv
    ```
    python -m venv .dg
    source .dg/bin/activate
    ```

- install the libraries
    ```
    pip install -r requirements.txt
    ```

- start mcp server for neo4j
    ```
    podman run -d --name neo4j-mcp-sse \
    -p 8000:8000 \
    -e NEO4J_URI=bolt://host.docker.internal:7687 \
    -e NEO4J_USERNAME=neo4j \
    -e NEO4J_PASSWORD=neoadmin \
    -e MCP_TRANSPORT=sse \
    quay.io/bjoydeep/neo4j-cypher:fixed
    ```
    - this server can be accessed at `http://localhost:8000/sse`



- start llama stack server
    - run 0.2.9 version
    - configure if it for OpenAI (this has not been tested on smaller models yet - WIP)

- copy the env-sample to .env and set the proper values

- Run llama stack agentic client
    ```
    streamlit run src/interface.py
    ```
    and start to chat



