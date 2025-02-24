import React, { useState, useEffect } from "react"

function AnimeCard(animeNodeData){
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)

    useEffect(() => {
        const fetchAnimeDetails = async () => {
            try {
                const response = await fetch('http://localhost:10001/testanimelistnode');
                if (!response.ok) {
                    throw new Error("erm ugh oh");
                }
                const result = await response.json();
                setData(result);
            } catch (e) {
                setError(e);
            } finally {
                setLoading(false);
            }
        };

        fetchAnimeDetails();
    }, []);

    if (loading) {
        return <p>Loading...</p>
    }

    if (error) {
        return <p>error: {error.message}</p>
    }

    return(
        <div className="card">
            <img src={data.main_picture.medium} alt="anime picture"></img>
            <h2>{data.title}</h2>
            <p>Anime Id : {data.id}</p>
        </div>
    )
}

export default AnimeCard