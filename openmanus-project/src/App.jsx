import { useState, useRef, useEffect } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Input } from '@/components/ui/input.jsx'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { ScrollArea } from '@/components/ui/scroll-area.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Loader2, Send, Bot, User, Terminal, Code, Globe, FileText, Image, Database } from 'lucide-react'
import './App.css'

function App() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      type: 'assistant',
      content: 'Hello! I\'m OpenManus, your AI agent. I can help you with various tasks including web browsing, coding, file editing, data analysis, and more. What would you like me to help you with today?',
      timestamp: new Date().toLocaleTimeString()
    }
  ])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [currentTask, setCurrentTask] = useState(null)
  const messagesEndRef = useRef(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!input.trim() || isLoading) return

    const userMessage = {
      id: Date.now(),
      type: 'user',
      content: input.trim(),
      timestamp: new Date().toLocaleTimeString()
    }

    setMessages(prev => [...prev, userMessage])
    setInput('')
    setIsLoading(true)

    try {
      // Get API URL from runtime environment or fallback
      const apiUrl = window.ENV?.API_URL || 'https://openmanus-backend-20u0.onrender.com'
      const response = await fetch(`${apiUrl}/api/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: input.trim() })
      })

      if (!response.ok) {
        throw new Error('Failed to get response')
      }

      const data = await response.json()
      
      const assistantMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: data.response || 'I understand your request. Let me work on that for you.',
        timestamp: new Date().toLocaleTimeString(),
        task: data.task || null,
        tools: data.tools || []
      }

      setMessages(prev => [...prev, assistantMessage])
      setCurrentTask(data.task || null)
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        type: 'assistant',
        content: 'I apologize, but I encountered an error processing your request. Please try again.',
        timestamp: new Date().toLocaleTimeString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const getToolIcon = (tool) => {
    switch (tool) {
      case 'browser': return <Globe className="w-4 h-4" />
      case 'code': return <Code className="w-4 h-4" />
      case 'terminal': return <Terminal className="w-4 h-4" />
      case 'file': return <FileText className="w-4 h-4" />
      case 'image': return <Image className="w-4 h-4" />
      case 'database': return <Database className="w-4 h-4" />
      default: return <Terminal className="w-4 h-4" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 dark:from-slate-900 dark:to-slate-800">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex items-center justify-center gap-3 mb-4">
            <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
              <Bot className="w-7 h-7 text-white" />
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
              OpenManus
            </h1>
          </div>
          <p className="text-slate-600 dark:text-slate-400 text-lg">
            Your AI Agent for Any Task
          </p>
        </div>

        {/* Current Task Display */}
        {currentTask && (
          <Card className="mb-6 border-blue-200 bg-blue-50 dark:bg-blue-950 dark:border-blue-800">
            <CardHeader className="pb-3">
              <CardTitle className="text-blue-800 dark:text-blue-200 text-lg flex items-center gap-2">
                <Loader2 className="w-5 h-5 animate-spin" />
                Current Task
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-blue-700 dark:text-blue-300">{currentTask}</p>
            </CardContent>
          </Card>
        )}

        {/* Chat Messages */}
        <Card className="mb-6 shadow-lg">
          <CardContent className="p-0">
            <ScrollArea className="h-[600px] p-4">
              <div className="space-y-4">
                {messages.map((message) => (
                  <div
                    key={message.id}
                    className={`flex gap-3 ${
                      message.type === 'user' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    {message.type === 'assistant' && (
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                    )}
                    <div
                      className={`max-w-[80%] rounded-lg px-4 py-3 ${
                        message.type === 'user'
                          ? 'bg-blue-600 text-white ml-auto'
                          : 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{message.content}</p>
                      {message.tools && message.tools.length > 0 && (
                        <div className="flex flex-wrap gap-2 mt-3">
                          {message.tools.map((tool, index) => (
                            <Badge key={index} variant="secondary" className="flex items-center gap-1">
                              {getToolIcon(tool)}
                              {tool}
                            </Badge>
                          ))}
                        </div>
                      )}
                      <div className="text-xs opacity-70 mt-2">
                        {message.timestamp}
                      </div>
                    </div>
                    {message.type === 'user' && (
                      <div className="w-8 h-8 bg-slate-300 dark:bg-slate-600 rounded-full flex items-center justify-center flex-shrink-0">
                        <User className="w-4 h-4 text-slate-600 dark:text-slate-300" />
                      </div>
                    )}
                  </div>
                ))}
                {isLoading && (
                  <div className="flex gap-3 justify-start">
                    <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-full flex items-center justify-center flex-shrink-0">
                      <Bot className="w-4 h-4 text-white" />
                    </div>
                    <div className="bg-slate-100 dark:bg-slate-800 rounded-lg px-4 py-3">
                      <div className="flex items-center gap-2">
                        <Loader2 className="w-4 h-4 animate-spin" />
                        <span className="text-slate-600 dark:text-slate-400">
                          Thinking...
                        </span>
                      </div>
                    </div>
                  </div>
                )}
              </div>
              <div ref={messagesEndRef} />
            </ScrollArea>
          </CardContent>
        </Card>

        {/* Input Form */}
        <Card className="shadow-lg">
          <CardContent className="p-4">
            <form onSubmit={handleSubmit} className="flex gap-3">
              <Input
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask me to help you with anything..."
                className="flex-1"
                disabled={isLoading}
              />
              <Button type="submit" disabled={isLoading || !input.trim()}>
                {isLoading ? (
                  <Loader2 className="w-4 h-4 animate-spin" />
                ) : (
                  <Send className="w-4 h-4" />
                )}
              </Button>
            </form>
          </CardContent>
        </Card>

        {/* Features */}
        <div className="mt-8 grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
          {[
            { icon: Globe, label: 'Web Browsing' },
            { icon: Code, label: 'Code Execution' },
            { icon: Terminal, label: 'Shell Commands' },
            { icon: FileText, label: 'File Editing' },
            { icon: Image, label: 'Image Generation' },
            { icon: Database, label: 'Data Analysis' }
          ].map((feature, index) => (
            <Card key={index} className="text-center p-4 hover:shadow-md transition-shadow">
              <feature.icon className="w-8 h-8 mx-auto mb-2 text-blue-600" />
              <p className="text-sm font-medium text-slate-700 dark:text-slate-300">
                {feature.label}
              </p>
            </Card>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App

