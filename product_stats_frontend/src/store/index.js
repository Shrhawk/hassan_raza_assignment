import { applyMiddleware, combineReducers, createStore, compose } from 'redux';
import { createLogger } from 'redux-logger';
import thunkMiddleware from 'redux-thunk';
import { alert } from '../store/reducers/alert.reducer';
import { auth } from '../store/reducers/auth.reducer';

function saveToLocalStorage(state) {
    const serializedState = JSON.stringify(state);
    localStorage.setItem('state', serializedState);
}

function loadFromLocalStorage() {
    const serializedState = localStorage.getItem('state');
    if (serializedState === null) return undefined;
    return JSON.parse(serializedState);
}

const composeEnhancers = window.__REDUX_DEVTOOLS_EXTENSION_COMPOSE__ || compose;
const presistedState = loadFromLocalStorage();
let middleware = [thunkMiddleware];

if (process.env.NODE_ENV !== 'production') {
    middleware = [...middleware, createLogger()];
}

const combineReduce = combineReducers({
    auth,
    alert
});

const store = createStore(
    combineReduce,
    presistedState,
    composeEnhancers(applyMiddleware(...middleware))
);
store.subscribe(() => saveToLocalStorage(store.getState()));
export default store;
