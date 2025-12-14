# Design System Documentation

## Overview

This document outlines the design system for the Khadamni job search platform, built with React, Tailwind CSS, shadcn/ui patterns, and Framer Motion.

## Design Philosophy

- **Modern SaaS Aesthetic**: Clean, professional, startup-friendly
- **Glassmorphism**: Subtle glass effects with backdrop blur
- **Smooth Animations**: Micro-interactions using Framer Motion
- **Accessibility First**: WCAG compliant, keyboard navigation
- **Mobile-First**: Responsive design starting from mobile

## Color Palette

### Primary Colors
- **Indigo**: `#6366f1` - Primary actions, links
- **Purple**: `#9333ea` - Accents, highlights
- **Teal**: `#14b8a6` - Secondary actions, success states

### Neutral Colors
- **Slate**: Base grays for text and backgrounds
- **White/Black**: High contrast for readability

### Gradients
- **Primary Gradient**: `from-indigo-600 via-purple-600 to-pink-500`
- **Accent Gradient**: `from-teal-400 via-cyan-500 to-blue-500`

## Typography

### Font Families
- **Display**: Poppins (headings, hero text)
- **Body**: Inter (body text, UI elements)

### Font Sizes
- **Hero**: 4xl - 7xl (48px - 72px)
- **Headings**: 2xl - 4xl (24px - 36px)
- **Body**: base (16px)
- **Small**: sm (14px)

## Components

### Button
- **Variants**: primary, secondary, outline, ghost, accent
- **Sizes**: sm, md, lg
- **States**: default, hover, active, disabled, loading
- **Animation**: Scale on hover/tap

### Card
- **Variants**: default, glass, hover
- **Rounded**: 2xl (16px)
- **Shadow**: md to xl on hover
- **Animation**: Fade in, slide up

### Input
- **Rounded**: xl (12px)
- **Border**: 1px with focus ring
- **States**: default, focus, error
- **Accessibility**: Proper labels, ARIA attributes

## Layout Patterns

### Container
- Max width: 7xl (1280px)
- Padding: Responsive (4px mobile, 8px desktop)

### Grid System
- 1 column (mobile)
- 2 columns (tablet)
- 3-4 columns (desktop)

### Spacing
- Consistent 4px base unit
- Common: 4, 6, 8, 12, 16, 20, 24

## Animations

### Entrance Animations
- **Fade In**: Opacity 0 → 1
- **Slide Up**: Translate Y 20px → 0
- **Scale In**: Scale 0.95 → 1

### Interactions
- **Hover**: Scale 1.02, shadow increase
- **Tap**: Scale 0.98
- **Duration**: 200-300ms for smooth feel

## Responsive Breakpoints

- **sm**: 640px
- **md**: 768px
- **lg**: 1024px
- **xl**: 1280px
- **2xl**: 1536px

## Accessibility

- **Color Contrast**: WCAG AA compliant
- **Keyboard Navigation**: Full support
- **Screen Readers**: Proper ARIA labels
- **Focus States**: Visible focus rings

## Dark Mode

- Automatic theme switching
- Maintains contrast ratios
- Smooth transitions between themes

## Component Structure

```
components/
├── ui/
│   ├── Button.tsx
│   ├── Card.tsx
│   ├── Input.tsx
│   └── Skeleton.tsx
└── layout/
    ├── Header.tsx
    ├── Footer.tsx
    └── Sidebar.tsx
```

## Usage Examples

### Button
```tsx
<Button variant="primary" size="lg" isLoading={false}>
  Get Started
</Button>
```

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

### Input
```tsx
<Input
  label="Email"
  type="email"
  placeholder="you@example.com"
  error={errors.email}
/>
```

## Best Practices

1. **Consistency**: Use design system components
2. **Spacing**: Use Tailwind spacing scale
3. **Colors**: Use semantic color tokens
4. **Animations**: Keep them subtle and purposeful
5. **Responsive**: Test on all breakpoints
6. **Accessibility**: Always include labels and ARIA

