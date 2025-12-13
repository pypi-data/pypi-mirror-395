// 游戏配置
const GRID_SIZE = 20;
const CELL_SIZE = 20;
const CANVAS_WIDTH = 400;
const CANVAS_HEIGHT = 400;
const GRID_WIDTH = CANVAS_WIDTH / CELL_SIZE;
const GRID_HEIGHT = CANVAS_HEIGHT / CELL_SIZE;

// 游戏状态
let canvas, ctx;
let snake = [];
let direction = { x: 1, y: 0 };
let nextDirection = { x: 1, y: 0 };
let food = { x: 0, y: 0 };
let score = 0;
let highScore = 0;
let gameRunning = false;
let gameLoop = null;

// DOM元素
const scoreElement = document.getElementById('score');
const highScoreElement = document.getElementById('high-score');
const gameOverElement = document.getElementById('gameOver');
const startScreenElement = document.getElementById('startScreen');
const finalScoreElement = document.getElementById('finalScore');
const restartBtn = document.getElementById('restartBtn');
const startBtn = document.getElementById('startBtn');

// 初始化游戏
function init() {
    canvas = document.getElementById('gameCanvas');
    ctx = canvas.getContext('2d');
    
    // 设置画布大小
    canvas.width = CANVAS_WIDTH;
    canvas.height = CANVAS_HEIGHT;
    
    // 加载最高分
    loadHighScore();
    
    // 初始化蛇
    resetGame();
    
    // 绑定事件
    bindEvents();
}

// 重置游戏
function resetGame() {
    // 初始化蛇（从中间开始，长度为3）
    snake = [
        { x: Math.floor(GRID_WIDTH / 2), y: Math.floor(GRID_HEIGHT / 2) },
        { x: Math.floor(GRID_WIDTH / 2) - 1, y: Math.floor(GRID_HEIGHT / 2) },
        { x: Math.floor(GRID_WIDTH / 2) - 2, y: Math.floor(GRID_HEIGHT / 2) }
    ];
    
    direction = { x: 1, y: 0 };
    nextDirection = { x: 1, y: 0 };
    score = 0;
    gameRunning = false;
    
    updateScore();
    generateFood();
    draw();
}

// 生成食物
function generateFood() {
    do {
        food = {
            x: Math.floor(Math.random() * GRID_WIDTH),
            y: Math.floor(Math.random() * GRID_HEIGHT)
        };
    } while (snake.some(segment => segment.x === food.x && segment.y === food.y));
}

// 更新游戏状态
function update() {
    if (!gameRunning) return;
    
    // 更新方向
    direction = { ...nextDirection };
    
    // 计算蛇头新位置
    const head = {
        x: snake[0].x + direction.x,
        y: snake[0].y + direction.y
    };
    
    // 检查墙壁碰撞
    if (head.x < 0 || head.x >= GRID_WIDTH || head.y < 0 || head.y >= GRID_HEIGHT) {
        gameOver();
        return;
    }
    
    // 检查自身碰撞
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver();
        return;
    }
    
    // 添加新头部
    snake.unshift(head);
    
    // 检查是否吃到食物
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        updateScore();
        generateFood();
    } else {
        // 移除尾部
        snake.pop();
    }
    
    draw();
}

// 绘制游戏
function draw() {
    // 清空画布
    ctx.fillStyle = '#f0f0f0';
    ctx.fillRect(0, 0, CANVAS_WIDTH, CANVAS_HEIGHT);
    
    // 绘制网格线（可选）
    ctx.strokeStyle = '#e0e0e0';
    ctx.lineWidth = 0.5;
    for (let i = 0; i <= GRID_WIDTH; i++) {
        ctx.beginPath();
        ctx.moveTo(i * CELL_SIZE, 0);
        ctx.lineTo(i * CELL_SIZE, CANVAS_HEIGHT);
        ctx.stroke();
    }
    for (let i = 0; i <= GRID_HEIGHT; i++) {
        ctx.beginPath();
        ctx.moveTo(0, i * CELL_SIZE);
        ctx.lineTo(CANVAS_WIDTH, i * CELL_SIZE);
        ctx.stroke();
    }
    
    // 绘制食物
    ctx.fillStyle = '#ff6b6b';
    ctx.beginPath();
    ctx.arc(
        food.x * CELL_SIZE + CELL_SIZE / 2,
        food.y * CELL_SIZE + CELL_SIZE / 2,
        CELL_SIZE / 2 - 2,
        0,
        Math.PI * 2
    );
    ctx.fill();
    
    // 绘制蛇
    snake.forEach((segment, index) => {
        if (index === 0) {
            // 蛇头
            ctx.fillStyle = '#4ecdc4';
            ctx.fillRect(
                segment.x * CELL_SIZE + 2,
                segment.y * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            );
            // 眼睛
            ctx.fillStyle = '#fff';
            const eyeSize = 3;
            const eyeOffset = 6;
            if (direction.x === 1) {
                // 向右
                ctx.fillRect(segment.x * CELL_SIZE + eyeOffset + 4, segment.y * CELL_SIZE + 5, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + eyeOffset + 4, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
            } else if (direction.x === -1) {
                // 向左
                ctx.fillRect(segment.x * CELL_SIZE + 5, segment.y * CELL_SIZE + 5, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 5, segment.y * CELL_SIZE + 12, eyeSize, eyeSize);
            } else if (direction.y === 1) {
                // 向下
                ctx.fillRect(segment.x * CELL_SIZE + 5, segment.y * CELL_SIZE + eyeOffset + 4, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + eyeOffset + 4, eyeSize, eyeSize);
            } else {
                // 向上
                ctx.fillRect(segment.x * CELL_SIZE + 5, segment.y * CELL_SIZE + 5, eyeSize, eyeSize);
                ctx.fillRect(segment.x * CELL_SIZE + 12, segment.y * CELL_SIZE + 5, eyeSize, eyeSize);
            }
        } else {
            // 蛇身
            ctx.fillStyle = '#45b7b8';
            ctx.fillRect(
                segment.x * CELL_SIZE + 2,
                segment.y * CELL_SIZE + 2,
                CELL_SIZE - 4,
                CELL_SIZE - 4
            );
        }
    });
}

// 改变方向
function changeDirection(newDirection) {
    // 防止反向移动
    if (newDirection.x === -direction.x && newDirection.y === -direction.y) {
        return;
    }
    nextDirection = newDirection;
}

// 处理键盘输入
function handleKeyPress(event) {
    if (!gameRunning && event.key !== 'Enter' && event.key !== ' ') {
        return;
    }
    
    switch(event.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
            event.preventDefault();
            changeDirection({ x: 0, y: -1 });
            break;
        case 'ArrowDown':
        case 's':
        case 'S':
            event.preventDefault();
            changeDirection({ x: 0, y: 1 });
            break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
            event.preventDefault();
            changeDirection({ x: -1, y: 0 });
            break;
        case 'ArrowRight':
        case 'd':
        case 'D':
            event.preventDefault();
            changeDirection({ x: 1, y: 0 });
            break;
    }
}

// 开始游戏
function startGame() {
    resetGame();
    gameRunning = true;
    startScreenElement.classList.add('hidden');
    gameOverElement.classList.add('hidden');
    
    if (gameLoop) {
        clearInterval(gameLoop);
    }
    gameLoop = setInterval(update, 150);
}

// 游戏结束
function gameOver() {
    gameRunning = false;
    clearInterval(gameLoop);
    
    // 更新最高分
    if (score > highScore) {
        highScore = score;
        saveHighScore();
        updateScore();
    }
    
    finalScoreElement.textContent = score;
    gameOverElement.classList.remove('hidden');
}

// 更新分数显示
function updateScore() {
    scoreElement.textContent = score;
    highScoreElement.textContent = highScore;
}

// 保存最高分
function saveHighScore() {
    localStorage.setItem('snakeHighScore', highScore.toString());
}

// 加载最高分
function loadHighScore() {
    const saved = localStorage.getItem('snakeHighScore');
    if (saved) {
        highScore = parseInt(saved, 10);
        updateScore();
    }
}

// 绑定事件
function bindEvents() {
    // 键盘事件
    document.addEventListener('keydown', handleKeyPress);
    
    // 按钮事件
    startBtn.addEventListener('click', startGame);
    restartBtn.addEventListener('click', startGame);
    
    // 移动端控制按钮
    document.getElementById('btnUp').addEventListener('click', () => {
        if (gameRunning) changeDirection({ x: 0, y: -1 });
    });
    document.getElementById('btnDown').addEventListener('click', () => {
        if (gameRunning) changeDirection({ x: 0, y: 1 });
    });
    document.getElementById('btnLeft').addEventListener('click', () => {
        if (gameRunning) changeDirection({ x: -1, y: 0 });
    });
    document.getElementById('btnRight').addEventListener('click', () => {
        if (gameRunning) changeDirection({ x: 1, y: 0 });
    });
    
    // 触摸控制（移动端滑动）
    let touchStartX = 0;
    let touchStartY = 0;
    
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        touchStartX = e.touches[0].clientX;
        touchStartY = e.touches[0].clientY;
    });
    
    canvas.addEventListener('touchend', (e) => {
        e.preventDefault();
        if (!gameRunning) return;
        
        const touchEndX = e.changedTouches[0].clientX;
        const touchEndY = e.changedTouches[0].clientY;
        
        const deltaX = touchEndX - touchStartX;
        const deltaY = touchEndY - touchStartY;
        
        const minSwipeDistance = 30;
        
        if (Math.abs(deltaX) > Math.abs(deltaY)) {
            // 水平滑动
            if (Math.abs(deltaX) > minSwipeDistance) {
                if (deltaX > 0) {
                    changeDirection({ x: 1, y: 0 }); // 右
                } else {
                    changeDirection({ x: -1, y: 0 }); // 左
                }
            }
        } else {
            // 垂直滑动
            if (Math.abs(deltaY) > minSwipeDistance) {
                if (deltaY > 0) {
                    changeDirection({ x: 0, y: 1 }); // 下
                } else {
                    changeDirection({ x: 0, y: -1 }); // 上
                }
            }
        }
    });
}

// 页面加载完成后初始化
window.addEventListener('DOMContentLoaded', init);

