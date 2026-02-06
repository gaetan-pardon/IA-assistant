import "./chatbot.css"
import { useEffect, useState } from "react";
import ReactMarkdown from "react-markdown";
import { useNavigate } from "react-router-dom"
import { createHistory, addMessageToHistory, fetchHistory, fetchHistoryById, deleteHistoryService } from "../../services/HistoryService";



export default function ChatBot() {
        const [ isAuthenticated, setIsAuthenticated ] = useState(null);
        const [ loading, setLoading ] = useState(true);
        const [ histories, setHistories ] = useState(null);
        const [ currentHistory, setCurrentHistory ] = useState(null);
        const [ messages, setMessages ] = useState([]);
        const [ inputText, setInputText ] = useState("");
        const [ loadingAIResponse, setLoadingAIResponse ] = useState(false);

        const navigate = useNavigate();
        
        useEffect(() => {
            fetchHistory().then((response) => {
                if (response.status === 200) {
                    setHistories(response.data);
                    setIsAuthenticated(true);
                }
            }).catch(() => {
                setHistories([]);
                setIsAuthenticated(false);
            }).finally(() => {
                setLoading(false);
            });
        }, []);
    
        const handleSendMessage = () => {
            if (loadingAIResponse)
                return;
            if (!currentHistory) {
                return;
            }
            if (inputText.trim()) {
                setMessages(prev => [...prev, { text: inputText, sender: "user" }]);
                setInputText("");
                setLoadingAIResponse(true);
                addMessageToHistory(currentHistory.id, inputText).then((response) => {
                    if (response.status === 200 && response.data?.messages) {
                        const formattedMessages = response.data.messages.map((msg) => ({
                            text: msg.content,
                            sender: msg.role === "assistant" ? "bot" : "user"
                        }));
                        setMessages(formattedMessages);
                    }
                }).catch((error) => {
                    console.error("Error sending message:", error);
                }).finally(() => {
                    setLoadingAIResponse(false);
                });
            }
        };

        const changeHistory = (history) => {
            setCurrentHistory(history);
            setMessages([]);
            fetchHistoryById(history.id).then((response) => {
                if (response.status === 200 && response.data?.messages) {
                    if (!Array.isArray(response.data.messages)) {
                        setMessages([]);
                        return;
                    }
                    if(response.data.messages.length === 0)
                    {
                        setMessages([]);
                        return;
                    }
                    setMessages(response.data.messages.map((msg) => ({
                        text: msg.content,
                        sender: msg.role === "assistant" ? "bot" : "user"
                    })));
                }
            }).catch((error) => {
                console.error("Error fetching history by ID:", error);
            });
        };

        const handleKeyPress = (e) => {
            if (e.key === "Enter") {
                handleSendMessage();
            }
        };

        const deleteHistory = (historyId) => {
            deleteHistoryService(historyId).then((response) => {
                if (response.status === 200) {
                    fetchHistory().then((response) => {
                        if (response.status === 200) {
                            setHistories(response.data);
                        }
                    }).catch(() => {
                        setHistories([]);
                    });
                    if (currentHistory.id === historyId) {
                        setCurrentHistory(null);
                        setMessages([]);
                    }
                }
            }).catch((error) => {
                console.error("Error deleting history:", error);
            });
        };

        if (loading) {
            return <div>Loading...</div>;
        }
        if (!isAuthenticated) {
            navigate("/login");
            return null;
        }

    return (
        <div className="chats-container">
            <section className="chats-list">
                <button className="new-chat-button" disabled={loadingAIResponse} onClick={() => {
                    createHistory().then((response) => {
                        if (response.status === 201) {
                            setCurrentHistory(response.data);
                            setMessages([]);
                            setHistories(prev => [...prev, response.data]);
                        }
                    }).catch((error) => {
                        console.error("Error creating history:", error);
                    });
                    fetchHistory().then((response) => {
                        if (response.status === 200) {
                            setHistories(response.data);
                        }
                    }).catch(() => {
                        setHistories([]);
                    });
                }}>+ Nouvelle conversation</button>
                <h3>Historiques</h3>
                {histories && histories.map((history) => (
                    <div key={history.id} className="chat-item-container">
                        <button key={history.id} className="chat-item" onClick={() => changeHistory(history)} disabled={currentHistory?.id === history.id || loadingAIResponse}>
                            <span>{history.name}</span>
                        </button>
                        <button onClick={() => deleteHistory(history.id)} disabled={loadingAIResponse}>🗑</button>
                    </div>
                ))}
            </section>
            {currentHistory && (
                <section className="chat">
                    <div className="messages-container">
                        {messages.length > 0 ? messages.map((message, index) => (
                            <div key={index} className={`message ${message.sender}`}>
                                <ReactMarkdown>{message.text}</ReactMarkdown>
                            </div>
                    )) : <div className="no-messages">Aucun message pour le moment. Commencez la conversation !</div>}
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
                        <button className="send-button" onClick={handleSendMessage} disabled={loadingAIResponse}>
                            Envoyer
                        </button>
                    </div>
                </section>
            )}
        </div>
    )
}