const TelegramBot = require('node-telegram-bot-api');
const sqlite3 = require('sqlite3').verbose();
const fs = require("fs");

//import schedule from 'node-schedule'
//schedule.scheduleJob('0 0 * * *', () => { ... })
//

const db = new sqlite3.Database('./database/database.db');
db.run("CREATE TABLE IF NOT EXISTS users (user_id INTEGER PRIMARY KEY, stage TEXT, admin BOOL, usr_name TEXT, days_left INTEGER)");

const token = '5173499293:AAEjTu3z7N-6rhpJxHhhDPV_gR85hlTc-LA';

const bot = new TelegramBot(token, {polling: true});

setInterval(() => {
    var date = new Date();
    if(date.getHours() === 22 && date.getMinutes() === 0){ 
        minus_day();
    }
}, 60000);

// get user from db by id
function get_user(usr_id) {
    return new Promise(
        (resolve, reject) => {
            if (typeof usr_id == typeof 1) {    // if input is user_id
                db.serialize(() => {
                    db.get('SELECT * FROM users WHERE user_id = ?', usr_id, (err, rows) => {
                        if (err) {reject(err);}
                        resolve(rows);
                    });
                });
            } else {                            // if input is user_name
                db.serialize(() => {
                    db.get('SELECT * FROM users WHERE usr_name = ?', usr_id, (err, rows) => {
                        if (err) {reject(err);}
                        resolve(rows);
                    });
                });
            }
        }
    );
}


// Setting user's stage
function set_stage(stage, usr_id) {
    const pr = db.prepare("UPDATE users SET stage = ? WHERE user_id = ?");
    pr.run(stage, usr_id);
    pr.finalize();
}


// Minus one day from every user
function minus_day() {
    db.all('SELECT * FROM users', (err, rows) => {
        rows.forEach(el =>{
            const pr = db.prepare("UPDATE users SET days_left = ? WHERE user_id = ?");
            pr.run(el.days_left - 1, el.user_id);
            pr.finalize();
        })
    });
}


// On every incomming message
bot.on('message', (msg) => {
    const chatId = msg.chat.id;
    const text = msg.text;
    var stage;
    
    var stage_temp = get_user(chatId).then(results => {
        // If user in database
        if (results) {
            stage = results.stage;
            if (results.days_left <= 0) {
                bot.sendMessage(chatId, "Ваша подписка окончена, обратитесь к @GAMch1k", {
                        reply_markup: {
                            resize_keyboard: true,
                            keyboard: [
                                ["Получить проценты"]
                            ]
                        }
                    });
                return;
            } else if (text == '/start') {
                const pr = db.prepare("UPDATE users SET user_id = ? WHERE usr_name = ?");
                pr.run(chatId, '@' + msg.chat.username);
                pr.finalize();
                set_stage('start', chatId);
                bot.sendMessage(chatId, "Привет! это такой вот бот и тут должно быть описание, но мне лень", {
                        reply_markup: {
                            resize_keyboard: true,
                            keyboard: [
                                ["Получить проценты"]
                            ]
                        }
                    });
                return;
            } else {
                fs.readFile("./jsons/final.json", "utf8", (err, jsonString) => {
                    if (err) {
                      console.log("FINAL FILE READ ERROR ", err);
                      return;
                    }
                    try {
                        const data = JSON.parse(jsonString).data;
                        data.forEach(el => {
                            setTimeout(() => {bot.sendMessage(chatId, el)}, data.indexOf(el) * 100);
                        });
                    } catch (err) {
                        console.log("Error parsing JSON string:", err);
                    }
                });
                return;
            }
        } else if (text == '/start') {
            const pr = db.prepare("INSERT OR REPLACE INTO users (user_id, stage, admin, usr_name, days_left) VALUES (?, ?, ?, ?, ?)");
            pr.run(chatId, "start", false, '@' + msg.chat.username,  0);
            pr.finalize();
            bot.sendMessage(chatId, "Привет! это такой вот бот и тут должно быть описание, но мне лень", {
                reply_markup: {
                    resize_keyboard: true,
                    keyboard: [
                        ["Получить проценты"]
                    ]
                }
            });
            return;
        }
    });
});