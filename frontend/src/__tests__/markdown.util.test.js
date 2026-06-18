import { describe, expect, it } from 'vitest'
import { markdownToText, renderMarkdown } from '@/utils/markdown'

describe('markdown utils', () => {
  it('renders common markdown syntax', () => {
    const html = renderMarkdown('# Title\n\n**Bold** and [link](https://example.com)')

    expect(html).toContain('<h1>Title</h1>')
    expect(html).toContain('<strong>Bold</strong>')
    expect(html).toContain('<a href="https://example.com">link</a>')
  })

  it('does not render raw html from article content', () => {
    const html = renderMarkdown('<img src=x onerror=alert(1)><script>alert(1)</script>')

    expect(html).not.toContain('<img')
    expect(html).not.toContain('<script>')
    expect(html).toContain('&lt;img')
  })

  it('extracts readable plain text from markdown', () => {
    expect(markdownToText('## Hello **world**\n\n[OpenAI](https://openai.com)')).toBe('Hello world OpenAI')
  })
})
