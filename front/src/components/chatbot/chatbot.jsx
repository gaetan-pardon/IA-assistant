import "./chatbot.css"
import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom"
import { createHistory, addMessageToHistory } from "../../services/HistoryService";



export default function ChatBot() {
        const [ isAuthenticated, setIsAuthenticated ] = useState(null);
        const [ loading, setLoading ] = useState(true);
        const [ currentHistory, setCurrentHistory ] = useState([]);
        const [ messages, setMessages ] = useState([]);
        const [ inputText, setInputText ] = useState("");

        const navigate = useNavigate();
        
        useEffect(() => {
            createHistory().then((response) => {
                if (response.status === 201) {
                    setCurrentHistory(response.data);
                    setIsAuthenticated(true);
                } else {
                    setIsAuthenticated(false);
                }
            }).catch((error) => {
                console.error("Error creating history:", error);
            }).finally(() => {
                setLoading(false);
            });
        }, []);
    
        const handleSendMessage = () => {
            if (inputText.trim()) {
                setMessages(prev => [...prev, { text: inputText, sender: "user" }]);
                setInputText("");
                addMessageToHistory(currentHistory.id, inputText).then((response) => {
                    if (response.status === 200 && response.data?.messages) {
                        const formattedMessages = response.data.messages.map((msg) => ({
                            text: msg.content,
                            sender: msg.role === "assistant" ? "bot" : "user"
                        }));
                        setMessages(formattedMessages);
                    }
                });
            }
        };

        const handleKeyPress = (e) => {
            if (e.key === "Enter") {
                handleSendMessage();
            }
        };

        if (loading) {
            return <div>Loading...</div>;
        } else if (!isAuthenticated) {
            navigate("/login");
            return null;
        }

    return (
        <section className="chat">
            <div className="messages-container">
                {messages.map((message, index) => (
                    <div key={index} className={`message ${message.sender}`}>
                        {message.text}
                    </div>
                ))}
            </div>
            
            <div className="input-container">
                <input
                    type="text"
                    className="prompt-input"
                    placeholder="Écrivez votre message..."
                    value={inputText}
                    onChange={(e) => setInputText(e.target.value)}
                    onKeyUp={handleKeyPress}
                />
                <button className="send-button" onClick={handleSendMessage}>
                    Envoyer
                </button>
            </div>
        </section>
    )
}