package eu.ludovicoottaviani.pyspotiwatchbe.controller;

import eu.ludovicoottaviani.pyspotiwatchbe.model.HistoryRow;
import eu.ludovicoottaviani.pyspotiwatchbe.service.HistoryRowService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.*;

import java.time.LocalDateTime;
import java.util.List;

@CrossOrigin("http://localhost:4200")
@RestController
@RequestMapping(value = "/history")
public class HistoryController {

    @Autowired
    private HistoryRowService historyRowService;

    @GetMapping("/list")
    public List<HistoryRow> findAll() {
        return historyRowService.findAll();
    }

    @PostMapping(value ="/insert", consumes = MediaType.APPLICATION_JSON_VALUE)
    public void insert(@RequestBody Object body) {
        HistoryRow row = new HistoryRow();
        row.setItems(body);
        row.setTime(LocalDateTime.now());
        historyRowService.insert(row);
    }

    @DeleteMapping(value = "/delete/{id}")
    public void delete(@PathVariable("id") String id) {
        historyRowService.delete(id);
    }
}