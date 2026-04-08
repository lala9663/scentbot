const data = JSON.parse(response.reply)

data.blogs.forEach(blog => {
  console.log(blog.title)
})

const sendMessage = async () => {
  const res = await sendChat({
    messages: [{ role: "user", content: input.value }],
    collection: [],
    wishlist: []
  })

  const data = JSON.parse(res.reply)

  recommendations.value = data.recommendations || []
  blogs.value = data.blogs || []
}