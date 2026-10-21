# Naija Market

- A marketplace website with shops and items.
- It has an AI chat helper. You type what you want, and the helper clicks and types on the page for you.

## What you need

- Python 3.14 (the project venv uses this)
- Node.js and npm
- Docker (for the database)
- An OpenRouter API key (get one at https://openrouter.ai)

## 1. Start the database

- Run this once to create the database:
  ```powershell
  docker run --name naija_marketplace_db -e POSTGRES_USER=naija_user -e POSTGRES_PASSWORD=naija_password -e POSTGRES_DB=naija_marketplace -p 5432:5432 -d postgres
  ```
- Next time, just start it again:
  ```powershell
  docker start naija_marketplace_db
  ```

## 2. Set up the backend

- Open a terminal in the project folder.
- Make a virtual environment:
  ```powershell
  python -m venv venvNaijApp
  ```
- Turn it on:
  ```powershell
  Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
  .\venvNaijApp\Scripts\Activate.ps1
  ```
- Install the packages:
  ```powershell
  pip install -r requirements.txt
  ```
- Make your settings file:
  ```powershell
  Copy-Item .env.example .env
  ```
- Open `.env` and replace `your_key_here` with your OpenRouter key.
- Create the database tables:
  ```powershell
  python -m backend.app.database.create_tables
  ```
- Optional: add a sample shop owner:
  ```powershell
  python -m backend.app.database.insert_data
  ```
  - It only adds one shop owner. Other sample data is turned off (commented out) in `backend/app/database/insert_data.py`.

## 3. Run the backend

- Run this from the project folder (not from inside `backend`):
  ```powershell
  uvicorn backend.app.main:app_api --reload
  ```
- It runs at http://127.0.0.1:8000
- To see all API routes, open http://127.0.0.1:8000/docs
- Keep this terminal open.

## 4. Run the frontend

- Open a second terminal.
- Run:
  ```powershell
  cd frontend_new
  npm install
  npm run dev
  ```
- Open http://localhost:5173 in your browser.
- Use this exact address. The backend only accepts requests from it.

## Quick check

- The marketplace page loads.
- You can open a shop.
- You can send a message in the chat box and get a reply.

## Common problems

- **Backend stops with "OPENROUTER_API_KEY is missing"**
  - Check that `.env` is in the project folder and has your key.
- **Database connection error**
  - Check that the Docker container is running: `docker ps`
- **"No module named backend"**
  - Run uvicorn from the project folder, not from inside `backend`.
- **Page loads but shows no shops**
  - Make sure the backend is running and the tables are created.
  - Shops and items are not added automatically. Add them through the app or the sample data script.
- **Script is blocked when turning on the venv**
  - Run the `Set-ExecutionPolicy` line from step 2 first.

## How the AI helper works

- Built with LangChain and LangGraph, using models through OpenRouter.
- It turns plain requests into actions on the React marketplace page.
- A LangGraph state graph with a router sends each model tool call to a click, type, key press or clear tool.
- These tools return action commands.
- The FastAPI backend sends the commands to the browser.
- The browser runs them on the live page.
- Skills load only when needed. This saves tokens.
- The helper does one tool call per turn. This keeps it steady and predictable.
- Chat memory is kept per thread, so it remembers the conversation.
- It first used an MCP server. This was replaced with built-in tools because MCP added extra work for no gain.

---

**NOT NEEDED TO RUN THE APP. DO NOT READ. THESE ARE PERSONAL DEVELOPER NOTES.**

---

To create react frontend project:
run - npm create vite@latest frontend_new
select - react
select - javascript


docker exec -it naija_marketplace_db psql -U naija_user -d naija_marketplace  

Create the page where usersbased on Id's have access to their Shop and can create an item and choose the categoryt heir iteam is in 

Create a system that can look at a consumers cart and assume based on whats on their what they could make(im thinking ai that has info on what foods can be made)

Create a system on the producer end where the system can look at a current producer catalog and say ok youre not making alot of money on these product but it seems like these products are doing well in this location pivot to them