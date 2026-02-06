import "./chatbot.css"
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom"



export default function ChatBot() {
        const [isAuthenticated, setIsAuthenticated] = useState(null);
        const [loading, setLoading] = useState(true);
        const [ history, setHistory] = useState([]);

        const navigate = useNavigate();
        
        useEffect(() => {
            async function getUserHistories() {
                try {
                    const response = await fetchHistory();
                    console.log("Fetch history response:", response);
                    if (response.status === 200) {
                        setIsAuthenticated(true);
                        setHistory(response.data);
                    } else {
                        setIsAuthenticated(false);
                    }
                } catch (error) {
                    setIsAuthenticated(false);
                } finally {
                    setLoading(false);
                }  
            }
            getUserHistories();
        }, []);
    
        if (loading) {
            return <div>Loading...</div>;
        } else if (!isAuthenticated) {
            /* navigate("/login"); */
            console.log("User not authenticated, redirecting to login...");
            return null;
        }

    return (
        <div className="chatbot-component">
            <h1>ChatBot</h1>
            <button onClick={async () => {
                const response = await createHistory(); /*createHistory*/
            } } >New conversation</button>
            <ul>
                {Array.isArray(history) && history.map(item => (
                    <li><h2>{item.name}</h2>
                    {Array.isArray(item.messages) && item.messages.map(message => (
                    <li key={message.id}>{message.content}</li> ))}
                    <form onSubmit={async (e) => {
                        e.preventDefault();
                        const formData = new FormData(e.target);
                        const content = formData.get("content");
                        await addMessageToHistory(item.id, content);
                    }}>
                        <input type="text" name="content" />
                        <button type="submit">Send</button>
                    </form>
                    </li>
                ))}
            </ul>
        </div>  
    )
}