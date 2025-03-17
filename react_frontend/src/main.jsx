import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router-dom'

createRoot(document.getElementById('root')).render(
    <StrictMode>
        <BrowserRouter>
			<Routes>
				<Route index element={
					<>
						<div style={{ textAlign: 'center', marginTop: '20px' }}>
							<h1>Hello World :D</h1>
							<h2>This app unfortunately has no UI/UX design yet!</h2>
							<h2>Please come back momentarily!!</h2>
						</div>
					</>
				}/>
			</Routes>
        </BrowserRouter>
    </StrictMode>
)
