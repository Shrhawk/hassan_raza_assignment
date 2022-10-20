import React from 'react';
import { Navigate, Route, Routes } from 'react-router-dom';
import './App.css';
import constants from './utils/constants';
import { Header } from './views/components/headerComponent';
import { Home } from './views/pages/home';
import  MainPage from './views/pages/mainpage/mainPage';
import  UserInfo  from './views/pages/userinfo/userInfo';

function App() {
    
    return (
        <div className="App">
            <Header />
            <div>
                <Routes>
                    <Route path={constants.homePath} element={<Home/>} />
                    <Route exact path={constants.mainPage} element={<MainPage/>} />
                    <Route exact path={constants.UserInfo} element={<UserInfo/>} />
                    <Route path="*" element={<Navigate to ={constants.homePath} />}/>               
                </Routes>
            </div>
        </div>
    );
}

export default App;
