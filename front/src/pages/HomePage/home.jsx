import "./home.css"
import { Link } from "react-router-dom"

export default function HomePage() {
    return (
        <main className="home">
            <section className="home-card">
                <div className="home-badge">Chat 2GP</div>
                <p className="home-subtitle">
                    Connecte-toi pour reprendre une conversation, ou crée un compte
                    pour commencer.
                </p>
                <div className="home-actions">
                    <Link className="home-button" to="/login">
                        Se connecter
                    </Link>
                    <Link className="home-button" to="/register">
                        S'inscrire
                    </Link>
                </div>
            </section>
        </main>
    )
}