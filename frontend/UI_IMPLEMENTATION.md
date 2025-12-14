# UI Implementation Guide

## Overview

This document provides implementation details for the Khadamni job search platform UI, built with React, Tailwind CSS, and Framer Motion.

## Component Structure

```
frontend/src/
├── components/
│   └── ui/
│       ├── Button.tsx          # Reusable button component
│       ├── Card.tsx             # Card components with variants
│       ├── Input.tsx            # Form input with validation
│       └── Skeleton.tsx         # Loading skeletons
├── pages/
│   ├── LandingPage.tsx          # Homepage with hero and features
│   ├── LoginPage.tsx            # Authentication page
│   ├── RegisterPage.tsx         # Registration with role selection
│   ├── JobSeekerDashboard.tsx   # Main dashboard for job seekers
│   ├── SalaryPredictionPage.tsx # ML salary prediction interface
│   └── JobRecommendationsPage.tsx # Job recommendations with filters
├── lib/
│   └── utils.ts                # Utility functions (cn helper)
└── index.css                   # Global styles and Tailwind config
```

## Key Design Decisions

### 1. Glassmorphism
- Used `backdrop-blur-xl` for glass effect
- Semi-transparent backgrounds with borders
- Creates depth and modern aesthetic

### 2. Gradient Accents
- Primary: Indigo → Purple → Pink
- Accent: Teal → Cyan → Blue
- Applied to buttons, text, and highlights

### 3. Animations
- **Entrance**: Fade in, slide up, scale in
- **Interactions**: Hover scale (1.02), tap scale (0.98)
- **Stagger**: Sequential delays for lists
- **Smooth**: 200-300ms duration

### 4. Typography
- **Display Font**: Poppins for headings
- **Body Font**: Inter for content
- **Gradient Text**: Applied to key phrases

### 5. Spacing & Layout
- Consistent 4px base unit
- Card padding: 6 (24px)
- Section spacing: 8 (32px)
- Container max-width: 7xl (1280px)

## Component Usage

### Button
```tsx
<Button 
  variant="primary" 
  size="lg" 
  isLoading={false}
  onClick={handleClick}
>
  Get Started
</Button>
```

**Variants**: primary, secondary, outline, ghost, accent
**Sizes**: sm, md, lg
**Features**: Loading state, hover/tap animations

### Card
```tsx
<Card glass hover>
  <CardHeader>
    <CardTitle>Title</CardTitle>
    <CardDescription>Description</CardDescription>
  </CardHeader>
  <CardContent>Content</CardContent>
</Card>
```

**Props**: glass (glassmorphism), hover (hover effects)

### Input
```tsx
<Input
  label="Email"
  type="email"
  placeholder="you@example.com"
  icon={Mail}
  error={errors.email}
  helperText="Enter your email address"
/>
```

**Features**: Icon support, error states, helper text

## Page Implementations

### Landing Page
- Hero section with gradient text
- Feature cards with icons
- Stats section
- CTA section
- Footer

### Authentication Pages
- Split layout (branding + form)
- Role selection (Register)
- Form validation
- Smooth transitions

### Dashboards
- Personalized greeting
- Quick stats cards
- Main content area
- Sidebar widgets

### ML Pages
- Clean input forms
- Animated results
- Confidence indicators
- Visual feedback

## Responsive Design

### Breakpoints
- Mobile: < 640px (1 column)
- Tablet: 640px - 1024px (2 columns)
- Desktop: > 1024px (3-4 columns)

### Mobile-First Approach
- Base styles for mobile
- Progressive enhancement for larger screens
- Touch-friendly button sizes
- Collapsible navigation

## Accessibility

### WCAG Compliance
- Color contrast ratios meet AA standards
- Keyboard navigation support
- ARIA labels on interactive elements
- Focus indicators visible

### Semantic HTML
- Proper heading hierarchy
- Form labels associated with inputs
- Button roles and states
- Landmark regions

## Performance

### Optimizations
- Lazy loading for images
- Code splitting for routes
- Memoization for expensive components
- Debounced search inputs

### Animation Performance
- GPU-accelerated transforms
- Will-change hints
- Reduced motion support
- Efficient re-renders

## Dark Mode

### Implementation
- CSS variables for theme colors
- Toggle mechanism
- Smooth transitions
- Persistent preference

### Color Adjustments
- Maintained contrast ratios
- Adjusted opacity values
- Darker backgrounds
- Lighter text

## Next Steps

1. **Add More Pages**:
   - Recruiter Dashboard
   - Job Posting Form
   - Country Recommendations Page

2. **Enhance Components**:
   - Dropdown/Select component
   - Modal/Dialog component
   - Toast notifications
   - Data tables

3. **Integration**:
   - Connect to API endpoints
   - Add state management (Zustand)
   - Implement authentication flow
   - Add error handling

4. **Testing**:
   - Component tests
   - E2E tests
   - Accessibility audits
   - Performance testing

## Development Commands

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Design Tokens

All design tokens are defined in:
- `tailwind.config.js` - Colors, spacing, typography
- `src/index.css` - CSS variables, custom utilities
- `DESIGN_SYSTEM.md` - Complete design system documentation

