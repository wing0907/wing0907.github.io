// src/components/Topbar.tsx

import { useState, useRef, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Logo from './Logo';

import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faRightFromBracket, faGear } from '@fortawesome/free-solid-svg-icons';

export default function Topbar() {
  const nav = useNavigate();
  
  const [isPopoverOpen, setIsPopoverOpen] = useState(false);
  const popoverRef = useRef<HTMLDivElement>(null);

  const isAuthenticated = !!localStorage.getItem('access_token');

  const handleLogout = () => {
    localStorage.removeItem('access_token');
    window.location.replace('/login');
  };
  
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (popoverRef.current && !popoverRef.current.contains(event.target as Node)) {
        setIsPopoverOpen(false);
      }
    };
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const handleEsc = (event: KeyboardEvent) => {
      if (event.key === 'Escape') {
        setIsPopoverOpen(false);
      }
    };
    window.addEventListener('keydown', handleEsc);
    return () => window.removeEventListener('keydown', handleEsc);
  }, []);

  return (
    <header className="topbar">
      <div className="topbarLeft" onClick={() => nav('/landing')} role="button" aria-label="홈으로">
        <Logo size={18} showWordmark />
      </div>

      <nav className="topbarNav">
        <button className="link" onClick={() => nav('/landing')}>지능형 리서치</button>
        <button className="link" onClick={() => nav('/cases')}>전략 시뮬레이션</button>
      </nav>

      <div className="topbarRight">
        {isAuthenticated ? (
          <div className="profile-container" ref={popoverRef}>
            <button className="profile-button" onClick={() => setIsPopoverOpen(!isPopoverOpen)}>
              <FontAwesomeIcon icon={faUser} className="default-user-icon" />
            </button>
            
            <div className={`profile-popover ${isPopoverOpen ? 'open' : ''}`}>
              <div className="popover-menu">
                <button className="popover-button" onClick={() => nav('/settings')}>
                  <FontAwesomeIcon icon={faGear} />
                  설정
                </button>
                <button className="popover-button logout-button" onClick={handleLogout}>
                  <FontAwesomeIcon icon={faRightFromBracket} />
                  로그아웃
                </button>
              </div>
            </div>
          </div>
        ) : (
          <button className="btn ghost sm" onClick={() => nav('/login')}>로그인</button>
        )}
      </div>
    </header>
  );
}