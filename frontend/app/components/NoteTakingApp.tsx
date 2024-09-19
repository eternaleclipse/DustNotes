"use client"

import { useState, useEffect } from "react"
import { PlusIcon, Trash } from "lucide-react"
import { Badge } from "@/components/ui/badge"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Dialog, DialogContent, DialogHeader, DialogTitle } from "@/components/ui/dialog"

interface Note {
  id: number
  title: string
  content: string
  tags: string[]
  created_at: string
  updated_at: string
}

export default function Component() {
  const [notes, setNotes] = useState<Note[]>([])
  const [searchResults, setSearchResults] = useState<Note[]>([])
  const [isAddingNote, setIsAddingNote] = useState(false)
  const [editingNote, setEditingNote] = useState<Note | null>(null)
  const [searchQuery, setSearchQuery] = useState("")

  useEffect(() => {
    fetchNotes()
  }, [])

  const fetchNotes = async () => {
    const response = await fetch('http://localhost:5000/api/notes')
    const data = await response.json()
    setNotes(data)
  }

  const handleAddNote = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    const form = event.currentTarget
    const formData = new FormData(form)
    const newNote = {
      title: formData.get('title') as string,
      content: formData.get('content') as string,
      tags: (formData.get('tags') as string).split(',').map(tag => tag.trim()),
    }

    const response = await fetch('http://localhost:5000/api/notes', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(newNote),
    })

    if (response.ok) {
      fetchNotes()
      setIsAddingNote(false)
    }
  }

  const handleEditNote = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!editingNote) return

    const form = event.currentTarget
    const formData = new FormData(form)
    const updatedNote = {
      ...editingNote,
      title: formData.get('title') as string,
      content: formData.get('content') as string,
      tags: (formData.get('tags') as string).split(',').map(tag => tag.trim()),
    }

    const response = await fetch(`http://localhost:5000/api/notes/${editingNote.id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(updatedNote),
    })

    if (response.ok) {
      fetchNotes()
      setEditingNote(null)
    }
  }

  const handleSearch = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!searchQuery.trim()) {
      setSearchResults([])
      return
    }

    const response = await fetch(`http://localhost:5000/api/search?q=${encodeURIComponent(searchQuery)}`)
    const data = await response.json()
    setSearchResults(data)
  }

  const displayedNotes = searchResults.length > 0 ? searchResults : notes

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">My Notes</h1>
      <form onSubmit={handleSearch} className="mb-4 flex gap-2">
        <Input
          type="text"
          placeholder="Search notes..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="flex-grow"
        />
      </form>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5 gap-4">
      <Card
          className="flex items-center justify-center h-48 cursor-pointer hover:bg-gray-100 transition-colors"
          onClick={() => setIsAddingNote(true)}
        >
          <Button variant="ghost" className="w-full h-full flex flex-col items-center justify-center">
            <PlusIcon className="h-8 w-8 mb-2" />
            <span className="text-sm font-semibold">New Note</span>
          </Button>
        </Card>
        {displayedNotes.map((note) => (
          <Card key={note.id} className="flex flex-col h-48" onClick={() => setEditingNote(note)}>
            <CardHeader className="p-3">
              <CardTitle className="text-sm">{note.title}</CardTitle>
            </CardHeader>
            <CardContent className="flex-grow p-3 pt-0">
              <p className="text-xs text-gray-600 line-clamp-3">{note.content}</p>
            </CardContent>
            <CardFooter className="p-3 pt-0">
              <div className="flex flex-wrap gap-1">
                {note.tags.map((tag) => (
                  <Badge key={tag} className="text-xs px-1 py-0">
                    {tag}
                  </Badge>
                ))}
              </div>
            <Button
              size="icon"
              className="m-1"
              onClick={async () => {
                const response = await fetch(`http://localhost:5000/api/notes/${note.id}`, {
                  method: 'DELETE',
                })

                if (response.ok) {
                  fetchNotes()
                }
              }}
            >
              <Trash className="h-4 w-4" />
            </Button>
            </CardFooter>
          </Card>
        ))}
      </div>

      <Dialog open={isAddingNote} onOpenChange={setIsAddingNote}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Add New Note</DialogTitle>
          </DialogHeader>
          <form onSubmit={handleAddNote} className="space-y-4">
            <Input name="title" placeholder="Title" autoComplete="off" required />
            <Textarea className="h-40" name="content" placeholder="Content" autoComplete="off" required />
            <Input name="tags" autoComplete="off" placeholder="Tags (comma-separated)" />
            <Button type="submit">Add Note</Button>
          </form>
        </DialogContent>
      </Dialog>

      <Dialog open={editingNote !== null} onOpenChange={() => setEditingNote(null)}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Note</DialogTitle>
          </DialogHeader>
          {editingNote && (
            <form onSubmit={handleEditNote} className="space-y-4">
              <Input name="title" defaultValue={editingNote.title} autoComplete="off" required />
              <Textarea name="content" className="h-40" defaultValue={editingNote.content} autoComplete="off" required />
              <Input name="tags" defaultValue={editingNote.tags.join(', ')} autoComplete="off" />
              <Button type="submit">Update Note</Button>
            </form>
          )}
        </DialogContent>
      </Dialog>
    </div>
  )
}
