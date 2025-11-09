import { render, screen } from "@testing-library/react";
import App from "./App";

test("한국어 포트폴리오가 기본으로 렌더된다", async () => {
  render(<App />);
  const heroName = await screen.findByRole("heading", { level: 1, name: /장우진/ });
  expect(heroName).toBeInTheDocument();
});
