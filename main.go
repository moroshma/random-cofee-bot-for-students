package main

import (
	"fmt"
	e "test/telegramBot/lib"

	tgbotapi "github.com/go-telegram-bot-api/telegram-bot-api/v5"
)

var numericKeyboard = tgbotapi.NewReplyKeyboard(
	tgbotapi.NewKeyboardButtonRow(
		tgbotapi.NewKeyboardButton("1"),
		tgbotapi.NewKeyboardButton("2"),
		tgbotapi.NewKeyboardButton("3"),
	),
	tgbotapi.NewKeyboardButtonRow(
		tgbotapi.NewKeyboardButton("4"),
		tgbotapi.NewKeyboardButton("5"),
		tgbotapi.NewKeyboardButton("6"),
	),
)

func main() {
	bot, err := tgbotapi.NewBotAPI("5819321087:AAEbXI4pI1F80kUCgZurdUDjTJQKohdan-U")
	if err != nil {
		e.Wrap("can't run bot: ", err)

	}

	//bot.Debug = true

	fmt.Printf("Authorized on account %s", bot.Self.UserName)

	u := tgbotapi.NewUpdate(0)
	u.Timeout = 60

	updates := bot.GetUpdatesChan(u)

	for update := range updates {
		if update.Message == nil { // ignore any non-Message updates
			continue
		}

		// Create a new MessageConfig. We don't have text yet,
		// so we leave it empty.

		msg := tgbotapi.NewMessage(update.Message.Chat.ID, update.Message.Text)

		// Extract the command from the Message.
		switch update.Message.Text {
		case "/start":
			msg.Text = "I understand /sayhi and /status."
		case "/sayhi":
			msg.Text = "Hi :)"
		case "/status":
			msg.Text = "I'm ok."
		case "/open":
			msg.ReplyMarkup = numericKeyboard
		case "/close":
			msg.ReplyMarkup = tgbotapi.NewRemoveKeyboard(true)
		default:
			msg.Text = "I don't know that command"
		}

		if _, err := bot.Send(msg); err != nil {
			e.Wrap("can't send message: ", err)
		}
	}
}
