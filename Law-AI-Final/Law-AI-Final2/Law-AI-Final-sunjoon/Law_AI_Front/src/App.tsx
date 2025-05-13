// src/App.tsx

// 페이지 라우팅(경로 관리)을 위한 라이브러리입니다.
import {
  Routes,
  Route,
  Navigate,
} from 'react-router-dom';

// CSS 스타일시트를 전역으로 적용합니다.
import './styles.css';

// 각 페이지 컴포넌트들을 가져옵니다.
import Landing from './pages/Landing';
import Signup from './pages/Signup';
import Login from './pages/Login';
import type { JSX } from 'react';

/**
 * 로그인 상태 확인
 * localStorage에 access_token이 있으면 로그인된 것으로 판단
 */
const isAuthenticated = () => !!localStorage.getItem('access_token');

/**
 * 보호된 라우트 컴포넌트
 * 인증되지 않으면 /login으로 리다이렉트
 */
function ProtectedRoute({ children }: { children: JSX.Element }) {
  if (!isAuthenticated()) return <Navigate to="/login" replace />;
  return children;
}

/**
 * 이 애플리케이션의 최상위 라우터 컴포넌트입니다.
 * URL 경로에 따라 어떤 페이지를 렌더링할지 결정합니다.
 */
export default function App() {
  return (
    <Routes>
      {/* '/' 경로 접속 시 /login으로 이동 */}
      <Route path="/" element={<Navigate to="/login" replace />} />

      {/* 로그인 필요 없는 페이지 */}
      <Route path="/login" element={<Login />} />
      <Route path="/signup" element={<Signup />} />

      {/* 보호된 페이지: 로그인해야만 접근 가능 */}
      <Route
        path="/landing"
        element={
          <ProtectedRoute>
            <Landing />
          </ProtectedRoute>
        }
      />

      {/* 정의되지 않은 경로는 /landing으로 이동 */}
      <Route path="*" element={<Navigate to="/landing" replace />} />
    </Routes>
  );
}