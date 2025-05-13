import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

export default function Login() {
  const nav = useNavigate();
  const [email, setEmail] = useState('');
  const [pw, setPw] = useState('');
  const [loading, setLoading] = useState(false);

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !pw.trim()) {
      alert('이메일과 비밀번호를 모두 입력해주세요.');
      return;
    }

    setLoading(true);
    try {
      const response = await axios.post('http://localhost:8000/api/auth/login', {
        email,
        password: pw,
      });

      // 성공하면 토큰 저장 후 이동
      const { access_token } = response.data;
      localStorage.setItem('access_token', access_token);
      setLoading(false);
      nav('/landing', { replace: true });
    } catch (err: any) {
      setLoading(false);
      if (err.response) {
        alert(err.response.data.detail || '로그인 실패');
      } else {
        alert('서버와 연결할 수 없습니다.');
      }
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '100vh',
        width: '100%',
      }}
    >
      <main
        style={{
          maxWidth: 420,
          width: '100%',
          padding: 20,
        }}
      >
        <div className="glass" style={{ padding: 20, borderRadius: 16 }}>
          <h1 style={{ marginTop: 0, marginBottom: 8 }}>로그인</h1>
          <p style={{ marginTop: 0, color: 'var(--muted)' }}>
            LawAI 계정으로 로그인하세요.
          </p>

          <form onSubmit={onSubmit} style={{ display: 'grid', gap: 12 }}>
            <label style={{ display: 'grid', gap: 6 }}>
              <span style={{ fontSize: 13, color: 'var(--muted)' }}>이메일</span>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="you@example.com"
                style={{
                  height: 42,
                  borderRadius: 12,
                  background: 'rgba(10,16,28,.55)',
                  border: '1px solid var(--border)',
                  color: 'var(--text)',
                  padding: '0 14px',
                }}
              />
            </label>

            <label style={{ display: 'grid', gap: 6 }}>
              <span style={{ fontSize: 13, color: 'var(--muted)' }}>비밀번호</span>
              <input
                type="password"
                value={pw}
                onChange={(e) => setPw(e.target.value)}
                placeholder="••••••••"
                style={{
                  height: 42,
                  borderRadius: 12,
                  background: 'rgba(10,16,28,.55)',
                  border: '1px solid var(--border)',
                  color: 'var(--text)',
                  padding: '0 14px',
                }}
              />
            </label>

            <div style={{ display: 'flex', gap: 8, justifyContent: 'flex-end' }}>
              <button
                type="button"
                className="btn"
                onClick={() => nav('/signup')}
              >
                회원가입
              </button>
              <button
                type="submit"
                className="btn primary"
                disabled={loading}
              >
                {loading ? '로그인 중…' : '로그인'}
              </button>
            </div>
          </form>
        </div>
      </main>
    </div>
  );
}
