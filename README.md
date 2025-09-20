# Sweet Shop Management System
A full-stack web application for managing an Indian sweet shop with user authentication, inventory management, and e-commerce functionality.

## 🍬 Features

### User Features
- **User Registration & Authentication**: Secure JWT-based authentication
- **Sweet Browsing**: View all available Indian sweets with images and descriptions
- **Search & Filter**: Search by name, filter by category and price range
- **Shopping Cart**: Add items to cart, modify quantities, and checkout
- **Purchase System**: Buy sweets individually or from cart
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile

### Admin Features
- **Inventory Management**: Add, edit, and delete sweets
- **Stock Control**: Restock items and track quantities
- **Category Management**: Organize sweets by Traditional, Bengali, Premium, South Indian
- **Price Management**: Update pricing and descriptions
- **Sales Monitoring**: View stock levels and manage inventory

### Technical Features
- **RESTful API**: Clean, well-documented API endpoints
- **Database Integration**: SQLite for development (easily configurable for PostgreSQL)
- **Real-time Updates**: Instant inventory updates after purchases
- **Image Management**: Sweet images with fallback support
- **Error Handling**: Comprehensive error handling and validation
- **CORS Support**: Configured for frontend-backend communication

## 🛠 Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: SQLite (Development) / PostgreSQL (Production)
- **ORM**: SQLAlchemy
- **Authentication**: JWT tokens with passlib bcrypt
- **API Documentation**: Auto-generated with FastAPI/Swagger

### Frontend
- **Framework**: React with TypeScript
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Icons**: Lucide React
- **Styling**: Custom CSS with modern design
- **State Management**: Context API for authentication

## 🚀 Local Setup Instructions

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- Git installed

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/sweet-shop-system.git
   cd sweet-shop-system
   ```

2. **Navigate to backend directory**
   ```bash
   cd backend
   ```

3. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create admin and user accounts**
   ```bash
   python create_admin.py
   ```

6. **Seed the database with sweet data**
   ```bash
   python seed_data.py
   ```

7. **Start the backend server**
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at: `http://localhost:8000`
   API Documentation: `http://localhost:8000/docs`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm start
   ```

   The application will be available at: `http://localhost:3000`

## 👤 Default Credentials

### Admin Account
- **Username**: `admin`
- **Password**: `admin123`
- **Features**: Full access to admin panel, inventory management

### Regular User Account  
- **Username**: `user`
- **Password**: `user123`
- **Features**: Browse and purchase sweets

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - User login
- `GET /api/auth/me` - Get current user info

### Sweets Management
- `GET /api/sweets` - Get all sweets
- `GET /api/sweets/search` - Search sweets
- `GET /api/sweets/{id}` - Get specific sweet
- `POST /api/sweets` - Create sweet (Admin only)
- `PUT /api/sweets/{id}` - Update sweet (Admin only)
- `DELETE /api/sweets/{id}` - Delete sweet (Admin only)

### Inventory
- `POST /api/sweets/{id}/purchase` - Purchase sweet
- `POST /api/sweets/{id}/restock` - Restock sweet (Admin only)

## 📱 Screenshots

### Dashboard View
<img width="1919" height="922" alt="image" src="https://github.com/user-attachments/assets/e4d74f24-40f3-4141-b28e-4a2ae2ad236d" />

*Browse and search through our collection of Indian sweets*

### Admin Panel
<img width="1919" height="909" alt="image" src="https://github.com/user-attachments/assets/523c4166-b44a-4144-b9b9-a6ea32d34d97" />

*Comprehensive inventory management interface*

### Shopping Cart
<img width="1919" height="907" alt="image" src="https://github.com/user-attachments/assets/80e4e2a1-6d50-47bf-8f3a-c1f3a211e671" />

*Easy-to-use shopping cart with quantity controls*



## 🧪 Testing

### Run Backend Tests
```bash
cd backend
pytest test_main.py -v
```

### Test Coverage
The test suite covers:
- User registration and authentication
- Sweet CRUD operations
- Purchase functionality
- Search and filtering
- Admin-only operations
- Error handling scenarios

## 🚀 Deployment

### Backend Deployment (Railway/Heroku)

1. **Update database URL for production**
   ```python
   # In database.py
   SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sweet_shop.db")
   ```

2. **Create requirements.txt**
   ```bash
   pip freeze > requirements.txt
   ```

3. **Deploy to Railway**
   - Connect your GitHub repository
   - Configure environment variables
   - Deploy automatically

### Frontend Deployment (Vercel/Netlify)

1. **Update API base URL**
   ```typescript
   // In AuthContext.tsx
   const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
   ```

2. **Build and deploy**
   ```bash
   npm run build
   ```

3. **Deploy to Vercel**
   - Connect GitHub repository
   - Configure build settings
   - Set environment variables

## 🎯 Future Enhancements

- **Order History**: Track user purchase history
- **Payment Integration**: Integrate with payment gateways
- **Email Notifications**: Order confirmations and updates
- **Advanced Analytics**: Sales reports and inventory analytics
- **Multi-language Support**: Hindi and regional language support
- **Bulk Operations**: Bulk inventory management
- **Customer Reviews**: Review and rating system
- **Discount System**: Coupons and promotional offers

## 🐛 Troubleshooting

### Common Issues

**Backend not starting:**
- Ensure Python 3.8+ is installed
- Check if virtual environment is activated
- Verify all dependencies are installed

**Database errors:**
- Delete `sweet_shop.db` and re-run setup scripts
- Check database permissions

**CORS errors:**
- Ensure backend server is running on port 8000
- Check CORS configuration in `main.py`

**Images not loading:**
- Check internet connection (images from external sources)
- Verify image URLs in database

## 📄 My AI Usage

### AI Tools Used
- **Claude (Anthropic)**: Primary development assistant
- **GitHub Copilot**: Code completion and suggestions during development

### How AI Was Used

1. **Initial Architecture Design**
   - Used Claude to design the overall system architecture
   - Generated the initial project structure and file organization
   - Created the database schema and API endpoint structure

2. **Backend Development**
   - AI assisted in writing FastAPI endpoints with proper error handling
   - Generated SQLAlchemy models and database relationships
   - Created authentication middleware and JWT token handling
   - Wrote comprehensive test cases following TDD principles

3. **Frontend Development**
   - Used AI to create React components with TypeScript
   - Generated responsive CSS styles and modern UI components
   - Implemented shopping cart functionality and state management
   - Created proper error handling and loading states

4. **Code Quality & Testing**
   - AI helped write unit tests for critical functionality
   - Generated mock data for testing and development
   - Assisted in code reviews and refactoring suggestions
   - Created comprehensive error handling patterns

5. **Documentation**
   - Used AI to generate API documentation
   - Created this comprehensive README with setup instructions
   - Generated inline code comments and docstrings

### AI Impact on Workflow

**Positive Impacts:**
- **Speed**: Reduced development time by ~60% with AI-generated boilerplate
- **Quality**: AI suggested best practices and error handling patterns
- **Testing**: Comprehensive test coverage with AI-generated test cases
- **Documentation**: Well-documented code with clear explanations

**Learning Experience:**
- AI served as a coding mentor, explaining concepts and best practices
- Helped understand FastAPI and React patterns more quickly
- Provided alternative solutions for complex problems
- Assisted in debugging and troubleshooting issues

The AI tools were instrumental in creating a production-ready application while maintaining high code quality and following industry best practices.

## 📞 Support

For issues or questions:
- Create an issue on GitHub
- Email: your-keshav21300@gmail.com
- Documentation: Check `/docs` folder for detailed guides

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI Team** for the excellent framework
- **React Team** for the powerful frontend library  
- **Indian Sweet Makers** for inspiring this delicious project
- **AI Assistants** for development support and guidance

---

**Made with ❤️ and AI assistance for the love of Indian sweets!**
