import { useState } from 'react'
import { getPageElements, executeAction } from '../agent/agentBridge'
import '../styles/components/AgentChat.css'

export default function AgentChat() {
    const [messages, setMessages] = useState([])
    const [input, setInput] = useState("")

    const[sessionId] = useState(() => crypto.randomUUID())

    const [open, setOpen] = useState(false)

    const send = async () => {
        if(!input.trim()) return
        const userMessage = input
        setInput("")

        // show user message in chat immediately
        setMessages(prev => [...prev, {role:"user", text: userMessage}])

        // snapshot the current DOM before sending
        // this is what the agent uses to know what elements are on screen
        const pageElements = getPageElements()

        const response = await fetch("http://localhost:8000/agent/chat", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({
                message: userMessage,
                thread_id: sessionId,
                page_elements: pageElements
            })
        })

        const data = await response.json()

        // execute each DOM action sequentially with a delay so the user
        // can visually see each step - type, then click, then press enter etc
        if(data.actions && data.actions.length > 0) {
            for (const action of data.actions) {
                executeAction(action)
                await new Promise(r => setTimeout(r, 400))
            }
        }

        // show the agent's final text response in the chat bubble
        setMessages(prev => [...prev, {role:"agent", text: data.response}])
    }

    return(
        <>
            <button className='chat-toggle' onClick={() => setOpen(!open)}>
                💬
            </button>

            {open && (
                <div className="agent-chat">

                    <div className="agent-header">
                        Naija Market Assistant
                    </div>

                    <div className="agent-messages">
                        {messages.map((m, i) => (
                            <div
                                key={i}
                                className={`message ${m.role}`}
                            >
                                {m.text}
                            </div>
                        ))}
                    </div>

                    <div className="agent-input-area">

                        <input
                            className="agent-input"
                            value={input}
                            onChange={e => setInput(e.target.value)}
                            onKeyDown={e => e.key === "Enter" && send()}
                            placeholder="Ask me anything..."
                        />

                        <button
                            className="send-button"
                            onClick={send}
                        >
                            ➜
                        </button>

                    </div>
                </div>
            )}
        </>
    )
}